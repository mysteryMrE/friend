import tkinter as tk

# Test basic image loading
root = tk.Tk()
root.withdraw()

try:
    # Test loading the image
    test_image = tk.PhotoImage(
        file="D:\\Dokumentumok\\SCHOOL\\IT_PROJECTS\\pets\\assets\\images\\idle_transparent.gif",
        format="gif -index 0",
    )
    print(f"Image loaded successfully: {test_image}")
    print(f"Image width: {test_image.width()}, height: {test_image.height()}")

    # Create a simple canvas to test
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.pack()

    # Test creating the image item
    item = canvas.create_image(0, 0, image=test_image, anchor="nw")
    print(f"Image item created: {item}")

    root.deiconify()
    root.mainloop()

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
