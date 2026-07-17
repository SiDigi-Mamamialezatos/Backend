import requests

BASE_URL = "https://sidigi-backend.vercel.app/api/materials/"

MODULE_ID = "ade21228-9665-4c2e-b8aa-33bef52926f2"

materials = [
    {
        "module_id": MODULE_ID,
        "title": "Jenis-jenis Penipuan Online",
        "narrative": [
            "Halo teman-teman! Namaku Digi, Detektif Internet! Hari ini kita akan belajar cara aman bermain internet.",
            "Di internet, ada orang jahat yang suka menipu. Yuk, kita kenali jenis-jenisnya!",
            "Pertama ada Phishing. Ini seperti memancing! Penipu menyamar jadi admin game atau bank untuk mencuri password-mu.",
            "Kedua, Toko Online Palsu! Gambarnya bagus, tapi saat dibeli... barangnya tidak pernah datang!",
            "Ketiga, Penipuan Hadiah dan Teman Palsu. Tiba-tiba ada yang bilang kamu menang undian, padahal bohong!",
            "Sekarang kamu sudah tahu jenis-jenisnya, kan? Lanjut ke pelajaran berikutnya, yuk!"
        ],
        "questions": [],
        "order": 0
    },
    {
        "module_id": MODULE_ID,
        "title": "Kenapa Penipu Mengincar Orang Tertentu",
        "narrative": [
            "Kalian tahu tidak, kenapa penipu suka mengincar kakek, nenek, atau orang yang sedang panik?",
            "Itu karena kakek dan nenek kita mungkin belum terbiasa memakai teknologi seperti kita.",
            "Penipu juga suka mencari orang yang sedang butuh uang, lalu menjanjikan uang cepat yang sebenarnya bohong.",
            "Orang yang sedang panik biasanya tidak bisa berpikir jernih. Makanya mereka mudah ditipu.",
            "Karena itu, kalian yang pintar internet ini harus membantu melindungi keluarga di rumah, ya!"
        ],
        "questions": [],
        "order": 1
    },
    {
        "module_id": MODULE_ID,
        "title": "Ciri-ciri Penipuan (Red Flags)",
        "narrative": [
            "Bagaimana cara mendeteksi penipuan? Gampang! Digi punya rahasianya.",
            "Tanda pertama: Mereka menyuruhmu BURU-BURU! \"Klik sekarang juga atau akunmu dihapus!\"",
            "Tanda kedua: Mereka minta kamu merahasiakannya dari ayah dan ibu. Hati-hati, ini sangat mencurigakan!",
            "Tanda ketiga: Minta ditransfer pakai cara aneh, seperti pakai pulsa atau voucher game.",
            "Tanda terakhir: Hadiahnya terlalu luar biasa! Kalau rasanya terlalu mustahil, itu pasti penipuan."
        ],
        "questions": [],
        "order": 2
    },
    {
        "module_id": MODULE_ID,
        "title": "Contoh Kasus Nyata di Lapangan",
        "narrative": [
            "Yuk, kita latihan jadi detektif! Bayangkan kamu dapat pesan SMS seperti ini...",
            "\"SELAMAT! Nomor Anda memenangkan Mobil Balap! Transfer pajak Rp 1 Juta sekarang untuk klaim hadiah!\"",
            "Wah! Ingat tanda tadi? Hadiah terlalu besar dan disuruh buru-buru bayar. Pasti penipuan!",
            "Atau ada WA dari nomor tak dikenal: \"Halo, ini paman. Paman pinjam uang ya, tolong rahasiakan dari ayahmu.\"",
            "Jangan langsung percaya! Selalu tanya ayah dan ibu dulu kalau dapat pesan aneh seperti itu."
        ],
        "questions": [],
        "order": 3
    },
    {
        "module_id": MODULE_ID,
        "title": "Apa yang Harus Dilakukan Kalau Tertipu",
        "narrative": [
            "Bagaimana kalau kita atau keluarga sudah terlanjur tertipu? Jangan panik, dan jangan menangis sendirian.",
            "Langkah pertama: JANGAN hapus pesannya! Segera screenshot atau foto layarnya sebagai bukti.",
            "Langkah kedua: Langsung lapor ke ayah, ibu, atau guru. Jangan malu, ini bukan salahmu.",
            "Orang dewasa akan membantu menelepon bank untuk memblokir rekening dan melapor ke polisi.",
            "Tetap waspada, tetap tenang, dan jadilah pahlawan internet yang pintar! Sampai jumpa di modul berikutnya!"
        ],
        "questions": [],
        "order": 4
    }
]

# =========================
# MODULE 2
# ID: 783144be-aff6-4086-a183-96d57050ea1c
# =========================

module2_id = "783144be-aff6-4086-a183-96d57050ea1c"

materials.extend([
    {
        "module_id": module2_id,
        "title": "Apa itu Pinjaman Online Jahat (Pinjol Ilegal)?",
        "narrative": [
            "Halo lagi, teman-teman! Detektif Digi kembali dengan misi baru.",
            "Terkadang, orang dewasa butuh meminjam uang dari internet. Ini disebut Pinjaman Online atau Pinjol.",
            "Tapi awas! Ada Pinjol jahat yang tidak punya izin. Mereka seperti monster penyedot uang!",
            "Di awal mereka bilang pinjamnya gampang, tapi nanti uang yang harus dikembalikan jadi sangat banyak.",
            "Kita harus ingatkan ayah, ibu, atau kakak agar tidak meminjam dari aplikasi yang tidak jelas, ya!"
        ],
        "questions": [],
        "order": 0
    },
    {
        "module_id": module2_id,
        "title": "Cara Kerja Pinjol Jahat",
        "narrative": [
            "Teman-teman tahu tidak kelicikan utama Pinjol jahat?",
            "Saat aplikasinya di-install, mereka akan diam-diam mencuri isi buku telepon dan fotomu!",
            "Kalau telat mengembalikan uang, mereka akan marah-marah dan mengirim pesan menakutkan.",
            "Yang lebih parah, mereka akan mengirim pesan jahat itu ke SEMUA teman dan keluargamu. Wah, itu namanya Bullying!",
            "Makanya, jangan pernah asal klik 'Izinkan' (Allow) kalau ada aplikasi yang minta akses ke kontak teleponmu!"
        ],
        "questions": [],
        "order": 1
    },
    {
        "module_id": module2_id,
        "title": "Cara Mengecek Pinjol yang Aman",
        "narrative": [
            "Terus, bagaimana cara tahu aplikasi itu aman atau jahat, Digi?",
            "Gampang! Kita harus jadi detektif dan mencari logo OJK!",
            "OJK itu singkatan dari Otoritas Jasa Keuangan. Mereka adalah Polisi Uang di Indonesia.",
            "Kalau aplikasi itu punya izin dari OJK, berarti mereka harus patuh pada aturan dan tidak boleh jahat.",
            "Kalau tidak ada logo OJK-nya? JAUHI SAJA! Jangan pernah di-download!"
        ],
        "questions": [],
        "order": 2
    },
    {
        "module_id": module2_id,
        "title": "Jebakan Bola Salju (Debt Trap)",
        "narrative": [
            "Pernahkah kalian melihat bola salju yang menggelinding dari atas gunung?",
            "Awalnya kecil, tapi lama-lama membesar menjadi raksasa! Itulah yang terjadi pada utang Pinjol jahat.",
            "Awalnya meminjam sedikit. Tapi karena ada 'bunga' atau denda yang tidak masuk akal, utangnya jadi membesar setiap hari!",
            "Banyak orang meminjam uang di aplikasi jahat lain untuk menutupi utang pertama. Itu seperti menggali lubang untuk menutup lubang!",
            "Itu namanya jebakan utang. Jangan sampai keluarga kita terjebak, ya."
        ],
        "questions": [],
        "order": 3
    },
    {
        "module_id": module2_id,
        "title": "Cara Melapor dan Meminta Bantuan",
        "narrative": [
            "Kalau ada keluarga atau kenalan yang diganggu Pinjol jahat, apa yang harus dilakukan?",
            "Pertama: BLOKIR nomor telepon penipu itu. Jangan dibalas dan jangan takut pada ancaman mereka.",
            "Kedua: Kumpulkan bukti screenshot pesannya, dan segera lapor ke Polisi Uang kita, yaitu OJK!",
            "Ketiga: Kalau mereka mengancam akan berbuat jahat, langsung laporkan ke Polisi sungguhan.",
            "Ingat, orang jahat hanya berani mengancam lewat handphone. Tetap berani dan jadilah pelindung keluargamu! Sampai jumpa di modul terakhir!"
        ],
        "questions": [],
        "order": 4
    }
])

# =========================
# MODULE 3
# ID: 95482e40-04d5-4ec3-9143-7983212fa6d9
# =========================

module3_id = "95482e40-04d5-4ec3-9143-7983212fa6d9"

materials.extend([
    {
        "module_id": module3_id,
        "title": "Ancaman Siber Umum (Virus & Pencuri Digital)",
        "narrative": [
            "Halo lagi! Di petualangan terakhir ini, kita akan belajar tentang monster-monster di dunia digital!",
            "Pertama ada Malware atau virus komputer. Mereka suka menyusup masuk dan merusak handphone atau komputer kita.",
            "Kedua ada Ransomware. Ini monster yang mengunci semua foto dan game milikmu, lalu meminta uang tebusan agar bisa dibuka lagi!",
            "Ada juga pencuri data dan SIM Swapping. Penjahat meniru nomor HP kita untuk mencuri akun rahasia. Seram sekali, kan?",
            "Tapi tenang, Digi akan ajari cara membuat tameng penangkalnya di pelajaran selanjutnya!"
        ],
        "questions": [],
        "order": 0
    },
    {
        "module_id": module3_id,
        "title": "Kata Sandi & Gembok Ganda (MFA)",
        "narrative": [
            "Cara pertama melindungi diri adalah dengan membuat Kata Sandi (Password) yang super kuat!",
            "Jangan pernah pakai sandi '123456' atau nama peliharaanmu. Itu terlalu mudah ditebak oleh penjahat!",
            "Gunakan campuran huruf besar, huruf kecil, dan angka. Buat seperti kalimat rahasia yang hanya kamu yang tahu.",
            "Lebih bagus lagi kalau kita pasang Gembok Ganda! Orang dewasa menyebutnya MFA atau Autentikasi Dua Langkah.",
            "Jadi, walaupun penjahat tahu sandimu, mereka tetap butuh kode rahasia dari HP-mu untuk bisa masuk. Aman deh!"
        ],
        "questions": [],
        "order": 1
    },
    {
        "module_id": module3_id,
        "title": "Melindungi Data Diri di Media Sosial",
        "narrative": [
            "Siapa di sini yang suka main media sosial atau nonton video online?",
            "Ssst... ada satu aturan penting. Jaga rahasia data pribadimu!",
            "Data pribadi itu seperti: nama lengkap, alamat rumah, nama sekolah, atau nomor telepon ayah dan ibu.",
            "Jangan pernah membagikan informasi itu di komentar atau video, karena orang jahat bisa tahu kamu ada di mana.",
            "Jadilah misterius di internet! Biarkan hanya keluarga dan teman aslimu yang tahu rahasiamu."
        ],
        "questions": [],
        "order": 2
    },
    {
        "module_id": module3_id,
        "title": "Menghindari Link dan Aplikasi Jahat",
        "narrative": [
            "Pernahkah kamu melihat link atau tombol yang tiba-tiba muncul di layar?",
            "STOP! Jangan asal klik! Kadang, itu adalah jebakan yang bisa memasukkan virus ke alatmu.",
            "Kalau mau download game atau aplikasi, selalu gunakan toko resmi seperti Play Store atau App Store.",
            "Kalau ada teman online yang mengirim link aneh dan menyuruhmu mengunduh sesuatu...",
            "Abaikan saja dan tanyakan dulu pada ayah atau ibu. Lebih baik aman daripada menyesal!"
        ],
        "questions": [],
        "order": 3
    },
    {
        "module_id": module3_id,
        "title": "Membuat Rencana Keamanan Keluarga",
        "narrative": [
            "Pelajaran terakhir! Keamanan digital adalah kerja sama tim, lho.",
            "Ajak ayah, ibu, dan kakak untuk membuat \"Aturan Internet Keluarga\". Kalian bisa membahasnya bersama di meja makan.",
            "Contohnya: Berjanji untuk tidak merahasiakan apapun kalau ada yang aneh di internet, dan sepakat soal batas waktu main HP.",
            "Jika kita semua bekerja sama, tidak akan ada penjahat internet yang bisa mengganggu keluarga kita!",
            "Hore! Kamu sudah lulus jadi Detektif Siber Cilik. Selalu ingat pesan Digi, dan sampai jumpa di petualangan berikutnya!"
        ],
        "questions": [],
        "order": 4
    }
])

for material in materials:
    response = requests.post(BASE_URL, json=material)

    print("=" * 60)
    print(f"Order : {material['order']}")
    print(f"Title : {material['title']}")
    print(f"Status: {response.status_code}")

    try:
        print(response.json())
    except Exception:
        print(response.text)