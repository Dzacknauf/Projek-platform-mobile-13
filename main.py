import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
# yayaya
# Fungsi untuk memuat data dari file JSON
def load_jadwal():
    with open('jadwal.json', 'r') as file:
        return json.load(file)

def load_tugas():
    with open('tugas.json', 'r') as file:
        return json.load(file)

# Fungsi untuk menyimpan data ke file JSON
def save_jadwal(new_jadwal):
    jadwal_data = load_jadwal()
    jadwal_data.append(new_jadwal)
    with open('jadwal.json', 'w') as file:
        json.dump(jadwal_data, file, indent=4)

def save_tugas(new_tugas):
    tugas_data = load_tugas()
    tugas_data.append(new_tugas)
    with open('tugas.json', 'w') as file:
        json.dump(tugas_data, file, indent=4)

class MyApp(App):
    def build(self):
        # Layout utama
        layout = BoxLayout(orientation='vertical')

        # Label judul
        title = Label(text="Jadwal Kuliah dan Tugas", font_size=24, size_hint=(1, 0.1))
        layout.add_widget(title)

        # Membuat ScrollView untuk menampilkan jadwal kuliah
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # Memuat data jadwal kuliah dari file JSON
        jadwal = load_jadwal()

        # Menampilkan jadwal kuliah dari data JSON
        for j in jadwal:
            jadwal_label = Label(
            text=f"{j['mata_kuliah']} ({j['dosen']}) | {j['waktu']} | {j['ruangan']}",
            size_hint_y=None, height=40)
            scroll_layout.add_widget(jadwal_label)


        # Memuat data tugas dari file JSON
        tugas = load_tugas()

        # Menampilkan tugas kuliah dari data JSON
        for t in tugas:
            tugas_label = Label(
                text=f"{t['mata_kuliah']} | {t['deskripsi']} | {t['deadline']}",
                size_hint_y=None, height=40)
            scroll_layout.add_widget(tugas_label)

        # Menambahkan ScrollView ke layout utama
        scroll_view = ScrollView()
        scroll_view.add_widget(scroll_layout)

        # Menambahkan scroll view ke layout utama
        layout.add_widget(scroll_view)

        # Menambahkan tombol untuk menambah jadwal kuliah dan tugas
        add_button = Button(text="Tambah Jadwal / Tugas", size_hint=(1, 0.1), on_press=self.on_add_button_press)
        layout.add_widget(add_button)

        return layout

    def on_add_button_press(self, instance):
        # Membuat form popup untuk menambah jadwal kuliah atau tugas
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input fields untuk mata kuliah, waktu, ruangan, deskripsi, deadline
        mata_kuliah_input = TextInput(hint_text="Mata Kuliah", size_hint_y=None, height=40)
        dosen_input = TextInput(hint_text="Nama Dosen", size_hint_y=None, height=40)
        waktu_input = TextInput(hint_text="Waktu", size_hint_y=None, height=40)
        ruangan_input = TextInput(hint_text="Ruangan", size_hint_y=None, height=40)
        deskripsi_input = TextInput(hint_text="Deskripsi Tugas", size_hint_y=None, height=40)
        deadline_input = TextInput(hint_text="Deadline", size_hint_y=None, height=40)

        # Tombol untuk menyimpan data
        save_button = Button(text="Simpan", size_hint_y=None, height=40, on_press=lambda x: self.save_data(mata_kuliah_input.text, waktu_input.text, ruangan_input.text, deskripsi_input.text, deadline_input.text))

        # Menambahkan input dan tombol ke layout popup
        popup_layout.add_widget(mata_kuliah_input)
        popup_layout.add_widget(dosen_input)
        popup_layout.add_widget(waktu_input)
        popup_layout.add_widget(ruangan_input)
        popup_layout.add_widget(deskripsi_input)
        popup_layout.add_widget(deadline_input)
        popup_layout.add_widget(save_button)

        # Membuat dan menampilkan popup
        popup = Popup(title="Tambah Jadwal atau Tugas", content=popup_layout, size_hint=(0.8, 0.7))
        popup.open()

    def save_data(self, mata_kuliah, waktu, ruangan, deskripsi, deadline):
        # Menambahkan jadwal atau tugas baru ke dalam file JSON
        if waktu and ruangan:  # Menambah jadwal
            new_jadwal = {
                "id": len(load_jadwal()) + 1,  # Membuat ID baru berdasarkan jumlah jadwal
                "mata_kuliah": mata_kuliah,
                "dosen": dosen,
                "waktu": waktu,
                "ruangan": ruangan
            }
            save_jadwal(new_jadwal)
            print(f"Jadwal baru disimpan: {new_jadwal}")
        elif deskripsi and deadline:  # Menambah tugas
            new_tugas = {
                "id": len(load_tugas()) + 1,  # Membuat ID baru berdasarkan jumlah tugas
                "mata_kuliah": mata_kuliah,
                "deskripsi": deskripsi,
                "deadline": deadline
            }
            save_tugas(new_tugas)
            print(f"Tugas baru disimpan: {new_tugas}")
        self.reload_app()

    def reload_app(self):
        # Fungsi untuk mereload aplikasi setelah menambahkan jadwal atau tugas
        self.stop()
        self.run()

if __name__ == '__main__':
    MyApp().run()
