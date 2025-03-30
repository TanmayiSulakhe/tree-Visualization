import tkinter as tk
import time

# Node class for Splay Tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Splay Tree Implementation
class SplayTree:
    def __init__(self, visualizer):
        self.root = None
        self.visualizer = visualizer  # GUI reference for visualization

    def insert(self, key):
        self.visualizer.update_message(f"Inserting {key} into the tree...")
        time.sleep(1)
        self.root = self._insert(self.root, key)
        #drawing tree after insertion 
        self.visualizer.draw_tree()
        time.sleep(1)

        #splay after insertion
        self.root = self._splay(self.root, key)
        self.visualizer.update_message(f"{key} inserted successfully!")
        self.visualizer.draw_tree()

    def _insert(self, root, key):
        if not root:
            return Node(key)

        self.visualizer.highlight_node(root, "yellow")

        if key == root.val:
            self.visualizer.update_message(f"{key} already exists")
            time.sleep(2)
            return root
        
        if key < root.val:
            self.visualizer.update_message(f"{key} < {root.val} so going left")
            time.sleep(2)
            root.left = self._insert(root.left, key)
        else:
            self.visualizer.update_message(f"{key} > {root.val} so going right")
            time.sleep(2)
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
            return None

        root = self._splay(root, key)
        self.visualizer.draw_tree()
        time.sleep(1)

        if root.val != key:
            self.visualizer.update_message(f"{key} does not exist.")
            time.sleep(1)
            return root  # Key not found

        if not root.left:
            self.visualizer.update_message(f"Right child is the new root")
            time.sleep(1)
            return root.right
        if not root.right:
            self.visualizer.update_message(f"Left child is the new root")
            time.sleep(1)
            return root.left

        new_root = self._splay(root.left, key)

        # self.visualizer.draw_tree()
        # time.sleep(1)

        self.visualizer.update_message(f"tree has both left and right child")
        time.sleep(1)

        self.visualizer.update_message(f"New root is {new_root.val}")
        time.sleep(1)

        new_root.right = root.right
        return new_root
    
    # when i insert 2, 3, 0 after inserting 0 i can only see 3 on the screen , 
    # then when i insert 4, i can only see 0 on the screen , 
    # then i see the entire tree, but since this is a recursive function there is no fix to this because of 
    #recursive calling

    def _splay(self, root, key):
        if not root or root.val == key:
            self.visualizer.update_message(f"Key {key} is now at root (or tree is empty).")
            return root  
        
        if key < root.val:
            if not root.left:
                self.visualizer.update_message(f"Key {key} not found in left subtree.")
                return root

            if key < root.left.val:  # Zig-Zig case (Left-Left)
                self.visualizer.update_message("Performing Zig-Zig (Left-Left) Rotation.")
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)

            elif key > root.left.val:  # Zig-Zag case (Left-Right)
                self.visualizer.update_message("Performing Zig-Zag (Left-Right) Rotation.")
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            if root.left:
                root = self._rotate_right(root)

        else:
            if not root.right:
                self.visualizer.update_message(f"Key {key} not found in right subtree.")
                return root

            if key > root.right.val:  # Zig-Zig case (Right-Right)
                self.visualizer.update_message("Performing Zig-Zig (Right-Right) Rotation.")
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)

            elif key < root.right.val:  # Zig-Zag case (Right-Left)
                self.visualizer.update_message("Performing Zig-Zag (Right-Left) Rotation.")
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            if root.right:
                root = self._rotate_left(root)

        # Only draw the final tree once the recursion completes
        self.visualizer.update_message(f"Final tree after splaying {key}.")
        
        return root


    def _rotate_left(self, x):
        y = x.right
        if not y:
            return x

        # Show rotation in a new window
        self._show_rotation(x, y, "Left Rotation")

        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        if not y:
            return x

        # Show rotation in a new window
        self._show_rotation(x, y, "Right Rotation")
        x.left = y.right
        y.right = x
        return y
    
    def _show_rotation(self, old_root, new_root, rotation_type):
        rotation_window = tk.Toplevel(self.visualizer.master)
        rotation_window.title(rotation_type)
        rotation_canvas = tk.Canvas(rotation_window, width=300, height=200, bg="white")
        rotation_canvas.pack()

        rotation_canvas.create_text(150, 20, text=rotation_type, font=("Arial", 14, "bold"), fill="red")

        # Draw the original nodes before rotation
        rotation_canvas.create_oval(130, 50, 170, 90, fill="lightblue")  # Old root
        rotation_canvas.create_text(150, 70, text=str(old_root.val), font=("Arial", 12, "bold"))

        if "Left" in rotation_type:
            # Left Rotation: Right child becomes new root
            rotation_canvas.create_oval(180, 100, 220, 140, fill="lightblue")  # Right child (new root)
            rotation_canvas.create_text(200, 120, text=str(new_root.val), font=("Arial", 12, "bold"))
        else:
            # Right Rotation: Left child becomes new root
            rotation_canvas.create_oval(80, 100, 120, 140, fill="lightblue")  # Left child (new root)
            rotation_canvas.create_text(100, 120, text=str(new_root.val), font=("Arial", 12, "bold"))

        # Draw rotation arrow
        rotation_canvas.create_text(150, 160, text="Rotating...", font=("Arial", 12, "bold"), fill="black")

        rotation_canvas.update()
        time.sleep(1.5)

        # Clear the canvas and draw the new rotated structure
        rotation_canvas.delete("all")

        rotation_canvas.create_text(150, 20, text="After " + rotation_type, font=("Arial", 14, "bold"), fill="red")

        rotation_canvas.create_oval(130, 50, 170, 90, fill="lightgreen")  # New root
        rotation_canvas.create_text(150, 70, text=str(new_root.val), font=("Arial", 12, "bold"))

        if "Left" in rotation_type:
            # Left Rotation: Old root moves down-left
            rotation_canvas.create_oval(80, 100, 120, 140, fill="lightblue")
            rotation_canvas.create_text(100, 120, text=str(old_root.val), font=("Arial", 12, "bold"))
        else:
            # Right Rotation: Old root moves down-right
            rotation_canvas.create_oval(180, 100, 220, 140, fill="lightblue")
            rotation_canvas.create_text(200, 120, text=str(old_root.val), font=("Arial", 12, "bold"))

        rotation_canvas.update()
        time.sleep(1.5)

        rotation_window.destroy()

        

# GUI Class using Tkinter
class SplayTreeVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Splay Tree Visualizer")

        self.splay_tree = SplayTree(self)

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
            self.splay_tree.insert(int(value))
            self.entry.delete(0, tk.END)

    def delete_value(self):
        value = self.entry.get()
        if value.isnumeric():
            self.splay_tree.delete(int(value))
            self.entry.delete(0, tk.END)

    def draw_tree(self):
        self.canvas.delete("all")
        self._draw_tree(self.splay_tree.root, 250, 50, 120)

    def _draw_tree(self, node, x, y, dx):
        if node:
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue", tags=f"node_{node.val}")
            self.canvas.create_text(x, y, text=str(node.val), font=("Arial", 12, "bold"))

            # Draw left and right connections
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
    app = SplayTreeVisualizer(root)
    root.mainloop()
