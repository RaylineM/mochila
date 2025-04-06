import tkinter as tk
from tkinter import ttk, messagebox
from itertools import combinations


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
        
        # Limpar os campos de entrada
        self.entry_name.delete(0, tk.END)
        self.entry_cost.delete(0, tk.END)
        self.entry_benefit.delete(0, tk.END)
    
    def solve_knapsack(self):
        if not self.items:
            messagebox.showerror("Erro", "Nenhum recurso adicionado.")
            return
        
        try:
            max_budget = float(self.entry_budget.get())
        except ValueError:
            messagebox.showerror("Erro", "Orçamento inválido.")
            return
        best_value = 0
        best_combination = []
        for r in range(1, len(self.items) + 1):
            for combo in combinations(self.items,r):
                total_cost = sum(item[1] for item in combo)
                total_benefit = sum(item[2] for item in combo)
                if total_cost <= max_budget and total_benefit > best_value:
                    best_value = total_benefit
                    best_combination = combo

        for row in self.tree_selected.get_children():
            self.tree_selected.delete(row)
    
        for item in best_combination:
            self.tree_selected.insert("","end", values=item)
        messagebox.showinfo("Resultado", f"Beneficío total: {best_value}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DisasterResourceAllocator(root)
    root.mainloop()
