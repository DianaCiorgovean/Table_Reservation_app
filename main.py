class RedBlackNode:
    def __init__(self, reservation_id, nr_guests, time, left=None, right=None, parent=None, color="red"):
        self.reservation_id = reservation_id
        self.nr_guests = nr_guests
        self.time = time
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color

    def __str__(self):
        return f"Reservation {self.reservation_id}: {self.nr_guests} guests at {self.time}"

class RedBlackTree:
    def __init__(self):
        self.nil = RedBlackNode(None, None, None, None, None, None, "black")
        self.root = self.nil

    def insert(self, reservation_id, nr_guests, time):
        new_node = RedBlackNode(reservation_id, nr_guests, time)
        self._insert(new_node)

    def _insert(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.time < x.time:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.time < y.time:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent.color == "red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    self._left_rotate(z.parent.parent)
        self.root.color = "black"

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, reservation_id):
        node = self._search(reservation_id)
        if node == self.nil:
            return
        y = node
        y_original_color = y.color
        if node.left == self.nil:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.nil:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == "black":
            self._delete_fixup(x)

    def _transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_fixup(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.right.color == "black":
                        w.left.color = "black"
                        w.color = "red"
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "black" and w.left.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    self._right_rotate(x.parent)
                    x = self.root
                x.color = "black"

    def search(self, reservation_id):
        node = self._search(reservation_id)
        if node == self.nil:
            return None
        else:
            return (node.reservation_id, node.nr_guests, node.time)

    def _search(self, reservation_id):
        node = self.root
        while node != self.nil and reservation_id != node.reservation_id:
            if reservation_id < node.reservation_id:
                node = node.left
            else:
                node = node.right
        return node



    def _minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    #afiseaza toate nodurile
    def print_tree(self):
        self._print_tree(self.root)
        #in cazul in care nu exista noduri
        if self.root == self.nil:
            print("Nu exista rezervari momentan.")

    def _print_tree(self, node):
        if node != self.nil:
            self._print_tree(node.left)
            print(node)
            self._print_tree(node.right)

if __name__ == "__main__":
        tree = RedBlackTree()

        while True:
            print("Bine ati venit!")
            print("Va rugam sa selectati optiunea dorita:")
            print("1. Rezervati o masa")
            print("2. Anulati o rezervare")
            print("3. Cautati o rezervare")
            print("4. Afisati toate rezervarile existente")
            print("5. Iesiti")
            #input-ul de la utilizator
            option = input("Introduceti optiunea: \n")




            if option == "1":
                print("Introduceti ID-ul rezervarii:")
                reservation_id = int(input())
                print("Introduceti numarul de persoane(sunt disponibile mese de maxim 15 persoane):")
                nr_guests = int(input())
                while nr_guests >= 15:
                    print("Va rugam sa reintroduceti numarul de persoane:")
                    nr_guests = int(input())
                print("Introduceti ora (spre exemplu 18):")
                time = input()
                tree.insert(reservation_id, nr_guests, time)
                print("Rezervarea a fost finalizata cu succes! \n")
            elif option == "2":
                print("Introduceti ID-ul rezervarii pentru anulare:")
                reservation_id = int(input())
                tree.delete(reservation_id)
                print("Rezervarea a fost anulata.\n")
            elif option == "3":
                reservation_id = int(input("Introduceti ID-ul rezervarii pentru cautare: "))
                reservation = tree.search(reservation_id)
                if reservation is not None:
                    print("Rezervare gasita:")
                    print("ID-ul rezervarii: " + str(reservation[0]))
                    print("Numarul de persoane: " + str(reservation[1]))
                    print("Ora la care este rezervarea: " + str(reservation[2]))
                    print("\n")
                else:
                    print("Rezervare inexistenta.\n")
            elif option == "4":
                print("Toate rezervarile:")
                tree.print_tree()
                print("\n")
            elif option == "5":
                print("Va asteptam sa reveniti curand! La revedere!")
                break
            else:
                print("Optiune invalida. Va rugam sa reincercati.")
                print("\n")



