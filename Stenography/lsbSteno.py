# Program Steganografi LSB Sederhana
# Diperlukan library Pillow untuk manipulasi gambar.
# Install dengan cara: pip install Pillow

from PIL import Image

def text_to_binary(text):
    """Mengubah string teks menjadi representasi biner."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Mengubah string biner kembali menjadi teks."""
    # Memisahkan string biner menjadi bagian 8-bit
    binary_chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ""
    for binary_char in binary_chars:
        # Mengonversi setiap bagian 8-bit menjadi karakter
        text += chr(int(binary_char, 2))
    return text

def encode(image_path, secret_message, output_path):
    """Menyembunyikan pesan rahasia di dalam sebuah gambar menggunakan metode LSB."""
    try:
        # Membuka gambar
        image = Image.open(image_path).convert('RGB')
        # Menambahkan delimiter unik untuk menandai akhir pesan
        secret_message += "####" 
        binary_message = text_to_binary(secret_message)
        
        message_length = len(binary_message)
        width, height = image.size
        
        # Memeriksa apakah gambar cukup besar untuk menampung pesan
        if message_length > width * height * 3:
            raise ValueError("Pesan terlalu panjang untuk disembunyikan di dalam gambar ini.")

        data_index = 0
        pixels = image.load()

        for y in range(height):
            for x in range(width):
                # Mendapatkan nilai RGB piksel
                r, g, b = pixels[x, y]
                
                # Memodifikasi LSB dari komponen Red
                if data_index < message_length:
                    r = (r & 0b11111110) | int(binary_message[data_index])
                    data_index += 1
                
                # Memodifikasi LSB dari komponen Green
                if data_index < message_length:
                    g = (g & 0b11111110) | int(binary_message[data_index])
                    data_index += 1
                
                # Memodifikasi LSB dari komponen Blue
                if data_index < message_length:
                    b = (b & 0b11111110) | int(binary_message[data_index])
                    data_index += 1
                
                # Menyimpan piksel yang sudah dimodifikasi
                pixels[x, y] = (r, g, b)

                if data_index >= message_length:
                    break
            if data_index >= message_length:
                break
        
        # Menyimpan gambar hasil steganografi (stego-object)
        image.save(output_path)
        print(f"Pesan berhasil disembunyikan di dalam '{output_path}'")
        
    except FileNotFoundError:
        print(f"Error: File gambar '{image_path}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi error: {e}")

def decode(stego_image_path):
    """Mengekstrak pesan rahasia dari sebuah stego-image."""
    try:
        image = Image.open(stego_image_path).convert('RGB')
        binary_message = ""
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Mengekstrak bit LSB dari setiap komponen warna
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)
        
        # Mencari delimiter untuk menemukan akhir pesan
        delimiter_binary = text_to_binary("####")
        delimiter_index = binary_message.find(delimiter_binary)
        
        if delimiter_index != -1:
            # Mengambil hanya bagian pesan sebelum delimiter
            secret_binary = binary_message[:delimiter_index]
            secret_message = binary_to_text(secret_binary)
            return secret_message
        else:
            return "Tidak ada pesan tersembunyi yang ditemukan (delimiter tidak ada)."
            
    except FileNotFoundError:
        return f"Error: File gambar '{stego_image_path}' tidak ditemukan."
    except Exception as e:
        return f"Terjadi error: {e}"

# --- Contoh Penggunaan ---
if __name__ == "__main__":
    # Sediakan gambar input dengan nama 'cover_image.png'
    # dan pastikan file ini ada di direktori yang sama dengan script.
    
    # Proses ENCODE
    pesan_rahasia = "MySunshine"
    encode('cover_image.png', pesan_rahasia, 'stego_image.png')
    
    # Proses DECODE
    pesan_ditemukan = decode('stego_image.png')
    print(f"Pesan yang berhasil diekstrak: {pesan_ditemukan}")