import { serve } from "bun";
import index from "./index.html";

const server = serve({
  routes: {
    // Serve index.html for all unmatched routes.

    "/*": async (req) => {
        const pathname = new URL(req.url).pathname;
        let file = Bun.file(`dist${pathname}`);
        if (await file.exists()) return new Response(file);
        file = Bun.file(`dist${pathname}.html`);          // try adding .html
        if (await file.exists()) return new Response(file);
        return new Response(Bun.file("dist/index.html")); // SPA fallback
    },

    "/api/hello": {
      async GET(req) {
        return Response.json({
          message: "Hello, world!",
          method: "GET",
        });
      },
      async PUT(req) {
        return Response.json({
          message: "Hello, world!",
          method: "PUT",
        });
      },
    },

    "/api/hello/:name": async req => {
      const name = req.params.name;
      return Response.json({
        message: `Hello, ${name}!`,
      });
    },
  },

  development: process.env.NODE_ENV !== "production" && {
    // Enable browser hot reloading in development
    hmr: true,

    // Echo console logs from the browser to the server
    console: true,
  },
});

console.log(`🚀 Server running at ${server.url}`);
