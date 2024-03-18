import os
os.system('cls')

from prettytable import PrettyTable

class Item:
    counter = 1

    def __init__(self, nama, harga, stok, id_roti=None):
        self.id = id_roti if id_roti is not None else Item.counter
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def __str__(self):
        return f"ID: {self.id} - {self.nama} - Rp{self.harga} - Stok: {self.stok}"

class Node:
    def __init__(self, item):
        self.item = item
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah_roti(self, item, pos=None):
        new_node = Node(item)

        if pos == "awal":
            new_node.next = self.head
            self.head = new_node
        elif pos == "akhir":
            if not self.head:
                self.head = new_node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
        elif pos == "antara":
            if not self.head or not self.head.next:
                print("Minimal dua node untuk menambah di antara.")
                return

            nama_sebelum = input("Masukkan nama roti sebelum posisi baru: ")
            current = self.head
            while current.next and current.next.item.nama != nama_sebelum:
                current = current.next

            if current.next:
                new_node.next = current.next
                current.next = new_node
            else:
                print(f"Roti dengan nama {nama_sebelum} tidak ditemukan.")
        else:
            print("Posisi tidak valid.")

    def hapus_roti(self, pos=None, nama=None):
        if not self.head:
            print("Linked list kosong. Tidak ada yang dapat dihapus.")
            return False

        if pos == "awal":
            self.head = self.head.next
        elif pos == "akhir":
            current = self.head
            if not current.next:
                self.head = None
                return True
            while current.next.next:
                current = current.next
            current.next = None
        elif pos == "antara":
            if not self.head or not self.head.next:
                print("Minimal dua node untuk menghapus di antara.")
                return False

            if not nama:
                print("Nama roti tidak boleh kosong.")
                return False

            nama_sebelum = input("Masukkan nama roti yang ingin dihapus: ")
            current = self.head

            # Menangani kasus penghapusan di awal
            if current.item.nama == nama_sebelum:
                self.head = self.head.next
                return True
            elif current.next and current.next.item.nama == nama_sebelum:
                current.next = current.next.next
                return True
            else:
                print(f"Roti dengan nama {nama_sebelum} tidak ditemukan.")
                return False
        else:
            print("Posisi tidak valid.")
            return False

    def tampilkan_roti(self):
        table = PrettyTable(["ID", "Nama", "Harga", "Stok"])
        current = self.head
        while current:
            table.add_row([current.item.id, current.item.nama, current.item.harga, current.item.stok])
            current = current.next
        return str(table)

    def ubah_roti(self, nama, harga_baru, stok_baru):
        current = self.head
        while current:
            if current.item.nama == nama:
                current.item.harga = harga_baru
                current.item.stok = stok_baru
                return True
            current = current.next
        return False

    def sort_roti(self, key="nama", ascending=True):
        if key not in ["nama", "harga", "stok", "id"]:
            print("Kunci pengurutan tidak valid.")
            return

        if not self.head or not self.head.next:
            return

        # Gunakan Quick Sort atau Merge Sort
        if input("Gunakan Quick Sort? (y/n): ").lower() == 'y':
            self.quick_sort(key=key, ascending=ascending)
        else:
            self.merge_sort(key=key, ascending=ascending)

    def merge_sort(self, key="harga", ascending=True):
        if not self.head or not self.head.next:
            return

        def merge_sort_recursive(lst):
            if not lst or not lst.next:
                return lst

            slow, fast = lst, lst.next
            while fast and fast.next:
                slow, fast = slow.next, fast.next.next

            left, right = lst, slow.next
            slow.next = None

            left = merge_sort_recursive(left)
            right = merge_sort_recursive(right)

            return merge(left, right)

        def merge(left, right):
            result = LinkedList()
            current_result = result.head

            while left and right:
                if (getattr(left.item, key) < getattr(right.item, key)) if ascending else (
                        getattr(left.item, key) > getattr(right.item, key)):
                    if not current_result:
                        result.head = Node(left.item)
                        current_result = result.head
                    else:
                        current_result.next = Node(left.item)
                        current_result = current_result.next
                    left = left.next
                else:
                    if not current_result:
                        result.head = Node(right.item)
                        current_result = result.head
                    else:
                        current_result.next = Node(right.item)
                        current_result = current_result.next
                    right = right.next

            while left:
                current_result.next = Node(left.item)
                current_result = current_result.next
                left = left.next

            while right:
                current_result.next = Node(right.item)
                current_result = current_result.next
                right = right.next

            return result.head

        self.head = merge_sort_recursive(self.head)

    def quick_sort(self, key="nama", ascending=True):
        def partition(start, end):
            pivot_index = start
            pivot = getattr(self.head.item, key)

            while start < end:
                while start < len(self) and (
                        (getattr(self[start].item, key) <= pivot) if ascending else
                        (getattr(self[start].item, key) >= pivot)):
                    start += 1

                while (getattr(self[end].item, key) > pivot) if ascending else (
                        getattr(self[end].item, key) < pivot):
                    end -= 1

                if start < end:
                    self[start].item, self[end].item = self[end].item, self[start].item

            self[pivot_index].item, self[end].item = self[end].item, self[pivot_index].item
            return end

        def quick_sort_recursive(start, end):
            if start < end:
                pivot = partition(start, end)
                quick_sort_recursive(start, pivot - 1)
                quick_sort_recursive(pivot + 1, end)

        quick_sort_recursive(0, len(self) - 1)

    def sort_by_id(self, ascending=True):
        self.merge_sort(key="id", ascending=ascending)

    def __getitem__(self, index):
        current = self.head
        for _ in range(index):
            if current:
                current = current.next
            else:
                raise IndexError("Index out of range.")
        if current:
            return current

    def __len__(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        result = ""
        current = self.head
        while current:
            result += str(current.item) + "\n"
            current = current.next
        return result

    def jump_search(self, key, search_by="id"):
        if search_by not in ["id", "nama"]:
            print("Kriteria pencarian tidak valid.")
            return None

        if search_by == "id":
            search_key = int(key)
            current = self.head
            while current:
                if current.item.id == search_key:
                    return current.item
                current = current.next
        else:
            current = self.head
            while current:
                if current.item.nama.lower() == key.lower():
                    return current.item
                current = current.next

        return None

# Function untuk menampilkan menu
def print_menu():
    print("--------------------------------------------------")
    print ("Hai! Selamat Datang")
    print ("Silahkan memilih menu operasi yang tersedia: ")
    print("1. Tambah Roti")
    print("2. Tampilkan Roti")
    print("3. Ubah Roti")
    print("4. Hapus Roti")
    print("5. Urutkan Roti")
    print("6. Cari Roti")
    print("7. Keluar")
    print("--------------------------------------------------")


# Contoh penggunaan
roti_list = LinkedList()

# Menambahkan beberapa jenis roti
roti_list.tambah_roti(Item("Roti Tawar", 5000, 20, 101), pos="akhir")
roti_list.tambah_roti(Item("Butter Croissant", 15000, 15, 102), pos="akhir")
roti_list.tambah_roti(Item("Choco Chip Cookies", 12000, 25, 103), pos="akhir")
roti_list.tambah_roti(Item("Macaron", 20000, 10, 104), pos="akhir")
roti_list.tambah_roti(Item("Mille Crepes", 7000, 5, 105), pos="akhir")
roti_list.tambah_roti(Item("Secret Menu", 50000, 2, 106), pos="akhir")

while True:
    print_menu()

    pilihan = input("Pilih menu (1-7): ")

    if pilihan == '1':
        nama = input("Masukkan nama roti: ")
        harga = float(input("Masukkan harga roti: "))
        stok = int(input("Masukkan stok roti: "))
        id_roti = int(input("Masukkan ID roti: "))
        roti_list.tambah_roti(Item(nama, harga, stok, id_roti), pos="akhir")
        print(f"Roti dengan ID {id_roti} berhasil ditambahkan.")
    elif pilihan == '2':
        print(roti_list.tampilkan_roti())
    elif pilihan == '3':
        nama = input("Masukkan nama roti yang ingin diubah: ")
        harga_baru = float(input("Masukkan harga baru roti: "))
        stok_baru = int(input("Masukkan stok baru roti: "))
        if roti_list.ubah_roti(nama, harga_baru, stok_baru):
            print("Roti berhasil diubah.")
        else:
            print(f"Roti dengan nama {nama} tidak ditemukan.")
    elif pilihan == '4':
        print("Pilih posisi penghapusan:")
        print("1. Di Awal")
        print("2. Di Akhir")
        print("3. Di Antara")
        posisi_pilihan_hapus = input("Pilih posisi (1-3): ")

        if posisi_pilihan_hapus == '1':
            if roti_list.hapus_roti(pos="awal"):
                print("Roti di awal berhasil dihapus.")
            else:
                print("Roti di awal tidak ditemukan atau tidak dapat dihapus.")
        elif posisi_pilihan_hapus == '2':
            if roti_list.hapus_roti(pos="akhir"):
                print("Roti di akhir berhasil dihapus.")
            else:
                print("Roti di akhir tidak ditemukan atau tidak dapat dihapus.")
        elif posisi_pilihan_hapus == '3':
            nama_hapus = input("Masukkan nama roti yang ingin dihapus: ")
            if roti_list.hapus_roti(pos="antara", nama=nama_hapus):
                print(f"Roti dengan nama {nama_hapus} berhasil dihapus.")
            else:
                print(f"Roti dengan nama {nama_hapus} tidak ditemukan atau tidak dapat dihapus.")
        else:
            print("Pilihan posisi tidak valid.")
    elif pilihan == '5':
        print("Pilih kriteria pengurutan:")
        print("1. Nama")
        print("2. Harga")
        print("3. Stok")
        print("4. ID")
        kriteria_pilihan = input("Pilih kriteria (1-4): ")

        ascending_pilihan = input("Pengurutan Ascending atau Descending? (a/d): ").lower()
        ascending = True if ascending_pilihan == 'a' else False

        if kriteria_pilihan == '1':
            roti_list.sort_roti(key="nama", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan nama.")
        elif kriteria_pilihan == '2':
            roti_list.sort_roti(key="harga", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan harga.")
        elif kriteria_pilihan == '3':
            roti_list.sort_roti(key="stok", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan stok.")
        elif kriteria_pilihan == '4':
            roti_list.sort_roti(key="id", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan ID.")
        else:
            print("Pilihan kriteria tidak valid.")
    elif pilihan == '6':
        print("Pilih kriteria pencarian:")
        print("1. ID")
        print("2. Nama")
        kriteria_pencarian = input("Pilih kriteria (1/2): ")

        if kriteria_pencarian == '1':
            key = input("Masukkan ID roti yang ingin dicari: ")
            result = roti_list.jump_search(key, search_by="id")
            if result:
                print("Roti ditemukan:")
                print(result)
            else:
                print("Roti tidak ditemukan.")
        elif kriteria_pencarian == '2':
            key = input("Masukkan nama roti yang ingin dicari: ")
            result = roti_list.jump_search(key, search_by="nama")
            if result:
                print("Roti ditemukan:")
                print(result)
            else:
                print("Roti tidak ditemukan.")
        else:
            print("Pilihan kriteria pencarian tidak valid.")
    elif pilihan == '7':
        print("Terima kasih. Keluar dari program.")
        break
    else:
        print("Pilihan tidak valid. Silakan pilih 1-7.")
