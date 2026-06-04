# Architecture

This is a full-stack TypeScript app using Bun as both the HTTP server and the bundler, with React on the frontend and Tailwind for styling. There is no separate build step in development — Bun handles everything at runtime.

## How the pieces fit together

```
Browser request
      │
      ▼
src/index.ts  ──── serves HTML shell ──▶  src/index.html
  (Bun server)                                   │
      │                                           │ loads as <script type="module">
      │                                           ▼
      │                                    src/frontend.tsx
      │                                    (React entry point)
      │                                           │ renders
      │                                           ▼
      │                                      src/App.tsx
      │                                           │ imports
      │                                           ├─ src/APITester.tsx
      │                                           ├─ src/index.css
      │                                           ├─ src/logo.svg
      │                                           └─ src/react.svg
      │
      └── handles /api/* routes directly
          (returns JSON responses)
```

Bun acts as the glue: it runs `index.ts` as a server process, but it also bundles and serves the frontend files on the fly. When the browser loads `index.html` and encounters `<script type="module" src="./frontend.tsx">`, Bun transparently compiles that TSX and its imports before sending them to the browser. In development, HMR (Hot Module Replacement) keeps the browser in sync without a full reload.

## `src/` files

### `index.ts` — Server entry point
**Called by:** `package.json` scripts — the `dev` and `start` scripts pass this path explicitly to the `bun` CLI (`bun --hot src/index.ts`).

The Bun HTTP server. Defines all backend routes:
- `/*` — catch-all that serves `index.html` (making this a SPA)
- `/api/hello` — example GET/PUT endpoint returning JSON
- `/api/hello/:name` — example parameterized endpoint

Also enables HMR and browser console mirroring in development.

### `index.html` — HTML shell
**Called by:** `index.ts` via a direct ES import (`import index from "./index.html"`). Bun's server understands HTML imports natively and uses the file as a response body for matched routes.

The single page the server sends for every non-API request. It contains a `<div id="root">` mount point and a `<script type="module" src="./frontend.tsx">` tag that bootstraps the React app.

### `frontend.tsx` — React entry point
**Called by:** `index.html` via `<script type="module" src="./frontend.tsx">`. When the browser requests this script, Bun compiles the TSX on the fly before sending it.

Mounts the React app into `#root`. The one notable detail is the HMR-safe root creation pattern:

```ts
(import.meta.hot.data.root ??= createRoot(elem)).render(app);
```

This preserves the React root across hot reloads so the DOM isn't torn down and recreated on every save.

### `App.tsx` — Root React component
**Called by:** `frontend.tsx` via `import { App } from "./App"`.

The top-level UI component. Currently renders the Bun + React starter layout: two animated logos, a heading, and the `APITester` widget. This is the main file to modify when building out the actual application UI.

### `APITester.tsx` — API test widget
**Called by:** `App.tsx` via `import { APITester } from "./APITester"`.

A small dev/demo component that lets you fire requests at the server's API endpoints from the browser and see the JSON response. It's a convenience tool from the starter template — not core app logic.

### `index.css` — Global styles
**Called by:** `App.tsx` via `import "./index.css"`. Bun's bundler processes this through the Tailwind plugin (configured in `bunfig.toml`) and injects it as a `<style>` tag in the browser.

Sets up the base theme: dark background, light text, a tiled animated SVG background pattern, and the `spin` keyframe animation used by the React logo. All other styling is done inline via Tailwind utility classes in the component files.

### `logo.svg` — Bun logo
**Called by:** three places, each using a direct reference:
- `index.html` — `<link rel="icon" href="./logo.svg">` (favicon)
- `App.tsx` — `import logo from "./logo.svg"` (logo image in the header)
- `index.css` — `url("./logo.svg")` (repeating tile in the background animation)

### `react.svg` — React logo
**Called by:** `App.tsx` via `import reactLogo from "./react.svg"`.

Used only as the spinning React logo image in the header.

## Project root files

### `build.ts` — Production build script
**Called by:** `package.json` `build` script, which passes this path explicitly to `bun run build.ts`. Not loaded automatically.

Clears the `dist/` directory, finds all `*.html` files under `src/`, and passes them to `Bun.build` as entrypoints. Bun traces all imports from those HTML files and produces a minified, browser-targeted bundle with source maps into `dist/`. The Tailwind plugin processes CSS during this step.

### `bunfig.toml` — Bun configuration
**Called by:** Bun automatically — it looks for `bunfig.toml` at the project root by convention whenever any `bun` command runs. No explicit reference needed.

Configures the Bun dev server to apply the Tailwind plugin when serving static files, and whitelists `BUN_PUBLIC_*` environment variables for exposure to the browser.

### `tsconfig.json` — TypeScript configuration
**Called by:** Bun and your editor automatically — both look for `tsconfig.json` at the project root by convention. No explicit reference needed.

Strict TypeScript with `moduleResolution: "bundler"` (Bun's mode, which allows importing `.tsx` files directly) and a `@/*` path alias that maps to `src/*`.

### `bun-env.d.ts` — Asset type declarations
**Called by:** TypeScript automatically — the compiler includes all `.d.ts` files found within the project root that are not excluded by `tsconfig.json`. No explicit reference needed.

Tells TypeScript how to type imports of `.svg` files (returns a URL string) and `.css`/`.module.css` files, so those imports don't cause type errors.

### `package.json` — Project manifest
**Called by:** Bun automatically — it looks for `package.json` at the project root by convention to resolve dependencies and scripts. No explicit reference needed.

Defines three scripts:
- `dev` — starts the server with `--hot` for HMR
- `start` — starts the server in production mode (no HMR)
- `build` — runs `build.ts` to produce the `dist/` bundle

Dependencies: React 19, Tailwind 4, and the `bun-plugin-tailwind` adapter.
