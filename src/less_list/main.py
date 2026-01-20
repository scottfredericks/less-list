def process_user_input(data):
    if data is None:
        print("No data received")
        return  # <--- Now ty knows 'data' cannot be None below context

    print(f"Processing: {data.upper()}")  # Passes!
