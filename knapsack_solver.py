import tkinter as tk
from tkinter import ttk, messagebox

class DisasterResourceAllocator:
    def __init__(self, root):
        self.root = root
        self.root.title("Alocação de Recursos para Desastres Climáticos")

        self.items = []
        self.budget = tk.DoubleVar(value=1000)

        self.create_widgets()

    def create_widgets(self):
        frame_left = tk.Frame(self.root, padx=10, pady=10)
        frame_left.grid(row=0, column=0, sticky="ns")

        tk.Label(frame_left, text="Adicionar Recurso").pack()
        tk.Label(frame_left, text="Nome").pack()
        self.entry_name = tk.Entry(frame_left)
        self.entry_name.pack()
        tk.Label(frame_left, text="Custo").pack()
        self.entry_cost = tk.Entry(frame_left)
        self.entry_cost.pack()
        tk.Label(frame_left, text="Benefício").pack()
        self.entry_benefit = tk.Entry(frame_left)
        self.entry_benefit.pack()
        tk.Button(frame_left, text="Adicionar", command=self.add_item).pack()

        tk.Label(frame_left, text="Orçamento Máximo:").pack()
        self.entry_budget = tk.Entry(frame_left, textvariable=self.budget)
        self.entry_budget.pack()
        tk.Button(frame_left, text="Resolver", command=self.solve_knapsack).pack()

        frame_right = tk.Frame(self.root, padx=10, pady=10)
        frame_right.grid(row=0, column=1, sticky="ns")

        tk.Label(frame_right, text="Recursos Disponíveis").pack()
        self.tree_items = ttk.Treeview(frame_right, columns=("Nome", "Custo", "Benefício"), show="headings")
        self.tree_items.heading("Nome", text="Nome")
        self.tree_items.heading("Custo", text="Custo")
        self.tree_items.heading("Benefício", text="Benefício")
        self.tree_items.pack()

        tk.Label(frame_right, text="Recursos Selecionados").pack()
        self.tree_selected = ttk.Treeview(frame_right, columns=("Nome", "Custo", "Benefício"), show="headings")
        self.tree_selected.heading("Nome", text="Nome")
        self.tree_selected.heading("Custo", text="Custo")
        self.tree_selected.heading("Benefício", text="Benefício")
        self.tree_selected.pack()

    def add_item(self):
        name = self.entry_name.get()
        try:
            cost = float(self.entry_cost.get())
            benefit = float(self.entry_benefit.get())
        except ValueError:
            messagebox.showerror("Erro", "Custo e Benefício devem ser números.")
            return

        self.items.append((name, cost, benefit))
        self.tree_items.insert("", "end", values=(name, cost, benefit))
        self.entry_name.delete(0, tk.END)
        self.entry_cost.delete(0, tk.END)
        self.entry_benefit.delete(0, tk.END)

    def solve_knapsack(self):
        if not self.items:
            messagebox.showerror("Erro", "Nenhum recurso adicionado.")
            return

        try:
            self.capacity = float(self.entry_budget.get())
        except ValueError:
            messagebox.showerror("Erro", "Orçamento inválido.")
            return

        self.best_value = 0
        self.best_solution = []
        self.curr_value = 0
        self.curr_weight = 0
        self.current_subset = []

        def search(k):
            if k == len(self.items):
                if self.curr_weight <= self.capacity and self.curr_value > self.best_value:
                    self.best_value = self.curr_value
                    self.best_solution = list(self.current_subset)
            else:
                search(k + 1)
                item = self.items[k]
                self.current_subset.append(item)
                self.curr_value += item[2]
                self.curr_weight += item[1]
                search(k + 1)
                self.current_subset.pop()
                self.curr_value -= item[2]
                self.curr_weight -= item[1]

        search(0)

        for row in self.tree_selected.get_children():
            self.tree_selected.delete(row)

        for item in self.best_solution:
            self.tree_selected.insert("", "end", values=item)

        messagebox.showinfo("Resultado", f"Benefício total: {self.best_value}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DisasterResourceAllocator(root)
    root.mainloop()
