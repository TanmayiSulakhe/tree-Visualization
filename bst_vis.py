import tkinter as tk
import time

# Node class for BST
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Binary Search Tree Implementation
class BST:
    def __init__(self, visualizer):
        self.root = None
        self.visualizer = visualizer  # GUI reference for visualization

    def insert(self, key):
        self.visualizer.update_message(f"Inserting {key} into the tree...")
        time.sleep(1)
        self.root = self._insert(self.root, key)
        self.visualizer.update_message(f"{key} inserted successfully!")
        self.visualizer.draw_tree()

    def _insert(self, root, key):
        if not root:
            return Node(key)

        self.visualizer.highlight_node(root, "yellow")
        self.visualizer.master.update()
        time.sleep(1)

        if key == root.val:
            self.visualizer.update_message(f"{key} already exists")
            time.sleep(1)
            return root
        elif key < root.val:
            self.visualizer.update_message(f"{key} < {root.val}, going left")
            time.sleep(1)
            root.left = self._insert(root.left, key)
        else:
            self.visualizer.update_message(f"{key} > {root.val}, going right")
            time.sleep(1)
            root.right = self._insert(root.right, key)

        return root

    def delete(self, key):
        self.visualizer.update_message(f"Deleting {key}...")
        time.sleep(1)
        self.root = self._delete(self.root, key)
        self.visualizer.update_message(f"{key} deleted successfully (if it existed).")
        self.visualizer.draw_tree()

    def _delete(self, root, key):
        if not root:
            self.visualizer.update_message(f"{key} not found.")
            time.sleep(1)
            return root

        self.visualizer.highlight_node(root, "yellow")
        self.visualizer.master.update()
        time.sleep(1)

        if key < root.val:
            self.visualizer.update_message(f"{key} < {root.val}, searching left")
            time.sleep(1)
            root.left = self._delete(root.left, key)
        elif key > root.val:
            self.visualizer.update_message(f"{key} > {root.val}, searching right")
            time.sleep(1)
            root.right = self._delete(root.right, key)
        else:
            self.visualizer.update_message(f"Found {key}, deleting...")
            time.sleep(1)
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            min_larger_node = self._min_value_node(root.right)
            self.visualizer.update_message(f"Replacing {key} with {min_larger_node.val}")
            time.sleep(1)

            root.val = min_larger_node.val
            root.right = self._delete(root.right, min_larger_node.val)

        return root

    def _min_value_node(self, root):
        current = root
        while current.left:
            self.visualizer.highlight_node(current, "yellow")
            self.visualizer.master.update()
            time.sleep(1)
            current = current.left
        return current

# GUI Class using Tkinter
class BSTVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("BST Visualizer")

        self.bst = BST(self)

        self.canvas = tk.Canvas(master, width=500, height=350, bg="white")
        self.canvas.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.insert_button = tk.Button(master, text="Insert", command=self.insert_value)
        self.insert_button.pack()

        self.delete_button = tk.Button(master, text="Delete", command=self.delete_value)
        self.delete_button.pack()

        self.message_label = tk.Label(master, text="Welcome!", fg="blue")
        self.message_label.pack()

        self.draw_tree()

    def insert_value(self):
        value = self.entry.get()
        if value.isnumeric():
            self.bst.insert(int(value))
            self.entry.delete(0, tk.END)

    def delete_value(self):
        value = self.entry.get()
        if value.isnumeric():
            self.bst.delete(int(value))
            self.entry.delete(0, tk.END)

    def draw_tree(self):
        self.canvas.delete("all")
        self._draw_tree(self.bst.root, 250, 50, 120)

    def _draw_tree(self, node, x, y, dx):
        if node:
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue", tags=f"node_{node.val}")
            self.canvas.create_text(x, y, text=str(node.val), font=("Arial", 12, "bold"))

            if node.left:
                self.canvas.create_line(x - 10, y + 10, x - dx + 10, y + 50, fill="black")
                self._draw_tree(node.left, x - dx, y + 50, dx // 2)

            if node.right:
                self.canvas.create_line(x + 10, y + 10, x + dx - 10, y + 50, fill="black")
                self._draw_tree(node.right, x + dx, y + 50, dx // 2)

    def highlight_node(self, node, color):
        if node:
            self.canvas.itemconfig(f"node_{node.val}", fill=color)
            self.master.update()

    def update_message(self, text):
        self.message_label.config(text=text)
        self.master.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = BSTVisualizer(root)
    root.mainloop()
