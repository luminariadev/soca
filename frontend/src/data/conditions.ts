import type { DiagnosticCondition } from '../types';

export const EYE_CONDITIONS: Record<string, DiagnosticCondition> = {
  'Normal': {
    id: 'normal',
    name: 'Normal (Mata Sehat)',
    latinName: 'Oculus Sanus',
    icd10: 'Z01.00',
    category: 'Fisiologis Sehat',
    description: 'Kornea jernih transparan, sklera putih bersih tanpa pelebaran vaskular abnormal, margin kelopak rata, dan pupil sentral responsif.',
    severity: 'Aman / Normal',
    symptoms: [
      'Penglihatan jernih dan fokus tanpa kabut',
      'Tidak ada rasa gatal, perih, atau sensasi mengganjal',
      'Produksi air mata seimbang dan sklera tampak putih cerah',
      'Refleks pupil simetris terhadap stimulasi cahaya'
    ],
    selfCare: [
      {
        title: 'Terapkan Aturan 20-20-20',
        desc: 'Setiap 20 menit menatap layar, pandang objek berjarak 20 kaki (6 meter) selama 20 detik untuk mengistirahatkan otot siliaris.',
        icon: 'timer'
      },
      {
        title: 'Nutrisi Karotenoid & Omega-3',
        desc: 'Konsumsi sayuran hijau gelap, wortel, telur, dan ikan berlemak kaya lutein dan zeaxanthin untuk menjaga pigmen makula.',
        icon: 'restaurant'
      },
      {
        title: 'Tidur Berkualitas 7-8 Jam',
        desc: 'Waktu tidur yang cukup memfasilitasi regenerasi epitel kornea dan pelumasan alami bola mata.',
        icon: 'bedtime'
      }
    ],
    restrictions: [
      'Hindari menatap layar gadget di ruangan gelap gulita',
      'Jangan mengucek mata dengan tangan yang belum dicuci',
      'Hindari paparan asap rokok dan hembusan AC langsung ke mata'
    ],
    redFlags: [
      'Segera periksa jika timbul kilatan cahaya mendadak (fotopsia)',
      'Timbul bintik hitam melayang yang bertambah banyak drastis (floaters)',
      'Sensasi bayangan tirai hitam menutupi sebagian lapang pandang'
    ],
    imageUrl: '/images/conditions/normal.jpg'
  },
  'Konjungtivitis': {
    id: 'konjungtivitis',
    name: 'Konjungtivitis (Mata Merah)',
    latinName: 'Conjunctivitis Acuta',
    icd10: 'H10.9',
    category: 'Inflamasi Sklera & Konjungtiva',
    description: 'Inflamasi atau infeksi pada selaput transparan (konjungtiva) yang melapisi kelopak mata dan menutupi sklera, memicu pelebaran pembuluh darah.',
    severity: 'Sedang',
    symptoms: [
      'Sklera mata tampak merah muda hingga merah pekat (hiperemia)',
      'Sensasi berpasir, mengganjal, panas, atau terbakar',
      'Keluar sekret lendir encer atau kental di sudut mata',
      'Kelopak mata lengket saat bangun tidur di pagi hari'
    ],
    selfCare: [
      {
        title: 'Kompres Dingin Fisiologis',
        desc: 'Tempelkan kain kasa/handuk bersih yang dibasahi air dingin selama 10 menit untuk vasokonstriksi dan meredakan radang.',
        icon: 'ac_unit'
      },
      {
        title: 'Air Mata Buatan (Artificial Tears)',
        desc: 'Teteskan pelumas mata bebas bahan pengawet (minidose) 3–4 kali sehari untuk membersihkan kotoran dan iritan.',
        icon: 'water_drop'
      },
      {
        title: 'Pembersihan Kelopak Higienis',
        desc: 'Gunakan kasa steril terpisah untuk mata kanan dan kiri saat menyeka kerak atau kotoran di sudut mata.',
        icon: 'cleaning_services'
      }
    ],
    restrictions: [
      'JANGAN MENGUCEK MATA: Memicu abrasi kornea dan menyebarkan infeksi ke mata sebelah',
      'HENTIKAN LENSA KONTAK: Lepas dan jangan gunakan sampai sembuh total (buang lensa yang terkontaminasi)',
      'JANGAN BERBAGI HANDUK/BANTAL: Sangat menular melalui kontak permukaan kain'
    ],
    redFlags: [
      'Nyeri tajam menusuk di dalam rongga bola mata',
      'Fotofobia ekstrem (sangat silau meski di cahaya ruangan biasa)',
      'Penurunan tajam penglihatan mendadak',
      'Keluar nanah hijau/kuning kental terus-menerus'
    ],
    imageUrl: '/images/conditions/konjungtivitis.jpg'
  },
  'Cataract': {
    id: 'cataract',
    name: 'Katarak Eksternal (Kekeruhan Lensa)',
    latinName: 'Cataracta Senilis / Traumatica',
    icd10: 'H26.9',
    category: 'Kekeruhan Lensa Pupil',
    description: 'Kekeruhan bertahap pada lensa alami mata yang terlihat keputihan atau keabu-abuan pada pupil, menghalangi cahaya masuk ke retina.',
    severity: 'Perlu Penanganan Cepat',
    symptoms: [
      'Penglihatan berangsur kabur seperti tertutup kabut atau kaca buram',
      'Silau berlebih saat melihat lampu kendaraan di malam hari (halos)',
      'Pupil tampak berwarna abu-abu, keputihan, atau kekuningan',
      'Warna tampak memudar atau menguning'
    ],
    selfCare: [
      {
        title: 'Pencahayaan Memadai',
        desc: 'Tingkatkan intensitas cahaya lampu meja saat membaca atau beraktivitas untuk meningkatkan kontras visual.',
        icon: 'lightbulb'
      },
      {
        title: 'Gunakan Kacamata Anti-UV & Polarized',
        desc: 'Pakai kacamata hitam berlabel UV400 di luar ruangan untuk memperlambat laju oksidasi protein lensa.',
        icon: 'eyeglasses'
      },
      {
        title: 'Konsultasi Bedah Fakoemulsifikasi',
        desc: 'Jadwalkan pemeriksaan ke dokter spesialis mata untuk evaluasi waktu penggantian lensa tanam (IOL).',
        icon: 'medical_services'
      }
    ],
    restrictions: [
      'Hindari mengemudi di malam hari jika silau lampu mengganggu fokus',
      'Hindari paparan sinar matahari terik langsung tanpa pelindung mata',
      'Jangan menunda pemeriksaan jika aktivitas sehari-hari mulai terganggu'
    ],
    redFlags: [
      'Hilang penglihatan mendadak di salah satu mata',
      'Mata merah disertai nyeri kepala hebat dan mual (indikasi glaukoma sekunder)'
    ],
    imageUrl: '/images/conditions/cataract.jpg'
  },
  'Bulging Eyes': {
    id: 'bulging-eyes',
    name: 'Bulging Eyes (Mata Menonjol / Proptosis)',
    latinName: 'Proptosis / Exophthalmos',
    icd10: 'H05.20',
    category: 'Anomali Periorbital & Tiroid',
    description: 'Penonjolan bola mata ke arah anterior melampaui margin orbita, umumnya berkaitan dengan Graves Ophthalmopathy atau inflamasi jaringan lunak orbita.',
    severity: 'Sedang',
    symptoms: [
      'Sklera bagian atas atau bawah tampak berlebih (terlihat jelas di atas iris)',
      'Kelopak mata tampak tertarik ke belakang (eyelid retraction)',
      'Mata terasa kering, tegang, atau seperti ada tekanan di belakang bola mata',
      'Penutupan kelopak mata tidak sempurna saat tidur (lagophthalmos)'
    ],
    selfCare: [
      {
        title: 'Pelumas Mata Kental (Gel/Salep Malam)',
        desc: 'Oleskan salep pelumas mata sebelum tidur untuk mencegah kornea mengering akibat kelopak tidak tertutup rapat.',
        icon: 'water_drop'
      },
      {
        title: 'Tinggikan Posisi Kepala Saat Tidur',
        desc: 'Gunakan bantal lebih tinggi untuk mengurangi kongesti vaskular dan pembengkakan jaringan orbita di pagi hari.',
        icon: 'single_bed'
      },
      {
        title: 'Pemeriksaan Panel Hormon Tiroid',
        desc: 'Segera lakukan tes lab FT4 dan TSH untuk mendeteksi kaitan dengan disfungsi tiroid autoimun.',
        icon: 'clinical_notes'
      }
    ],
    restrictions: [
      'STOP MEROKOK TOTAL: Merokok memperparah penonjolan jaringan retrobulbar hingga 4x lipat',
      'Hindari paparan angin kencang atau debu tanpa kacamata pelindung tertutup',
      'Jangan menekan atau menekan paksa bola mata'
    ],
    redFlags: [
      'Penglihatan ganda (diplopia) saat melirik ke arah tertentu',
      'Penurunan saturasi warna (warna merah tampak memudar), tanda kompresi saraf optik'
    ],
    imageUrl: '/images/conditions/bulging-eyes.jpg'
  },
  'Crossed Eyes': {
    id: 'crossed-eyes',
    name: 'Crossed Eyes (Strabismus / Juling)',
    latinName: 'Strabismus Convergens / Divergens',
    icd10: 'H49.9',
    category: 'Ketidaksejajaran Sumbu Bola Mata',
    description: 'Deviasi arah penglihatan di mana sumbu optik kedua bola mata tidak tertuju secara paralel pada satu titik fokus (esotropia atau eksotropia).',
    severity: 'Ringan',
    symptoms: [
      'Satu bola mata melenceng ke arah hidung atau ke arah luar',
      'Kesulitan mengukur jarak benda atau persepsi kedalaman ruang 3D',
      'Cenderung memiringkan kepala saat mencoba fokus pada objek',
      'Kelelahan mata dan sakit kepala setelah membaca lama'
    ],
    selfCare: [
      {
        title: 'Terapi Penglihatan & Latihan Konvergensi',
        desc: 'Lakukan senam otot ekstraokular (seperti pensil push-up) sesuai panduan spesialis mata atau optometris.',
        icon: 'fitness_center'
      },
      {
        title: 'Evaluasi Kacamata Prisma',
        desc: 'Pemeriksaan refraksi lengkap untuk koreksi indeks bias yang mungkin menjadi pemicu akomodatif strabismus.',
        icon: 'eyeglasses'
      },
      {
        title: 'Istirahatkan Mata Berkala',
        desc: 'Kurangi ketegangan binokular saat bekerja di depan komputer dengan menjeda pandangan setiap 20 menit.',
        icon: 'pause_circle'
      }
    ],
    restrictions: [
      'Hindari membaca materi cetak atau layar dalam posisi berbaring miring',
      'Jangan abaikan gejala pada anak-anak untuk mencegah ambliopia (mata malas permanen)'
    ],
    redFlags: [
      'Timbul strabismus mendadak pada orang dewasa disertai sakit kepala berat atau kebas wajah'
    ],
    imageUrl: '/images/conditions/crossed-eyes.jpg'
  },
  'Dark Circles + Eyebags': {
    id: 'dark-circles',
    name: 'Dark Circles & Eyebags (Kantung Mata)',
    latinName: 'Periorbital Hyperpigmentation & Infraorbital Edema',
    icd10: 'L81.8',
    category: 'Estetika & Sirkulasi Periorbital',
    description: 'Hiperpigmentasi melanin kulit di bawah mata yang dikombinasikan dengan pelemahan septum orbita atau retensi cairan limfatik.',
    severity: 'Ringan',
    symptoms: [
      'Bayangan kehitaman, kebiruan, atau kecokelatan di area kelopak bawah',
      'Pembengkakan atau tonjolan bantalan lemak di bawah mata (eyebags)',
      'Kulit area periorbital tampak tipis dan vaskulatur membayang',
      'Mata tampak lelah atau sayu'
    ],
    selfCare: [
      {
        title: 'Kompres Dingin / Sendok Sejuk',
        desc: 'Tempelkan sendok dingin atau kantung teh hijau bekas pakai (kaya kafein) untuk vasokonstriksi mikrovaskular.',
        icon: 'coffee'
      },
      {
        title: 'Hidrasi Cairan Cukup (2 Liter/Hari)',
        desc: 'Minum air putih memadai dan kurangi asupan garam/sodium tinggi sebelum tidur untuk mencegah retensi cairan.',
        icon: 'water'
      },
      {
        title: 'Krim Mata Mengandung Kafein & Peptida',
        desc: 'Gunakan serum mata yang merangsang drainase limfatik dan sintesis kolagen periorbital.',
        icon: 'spa'
      }
    ],
    restrictions: [
      'Hindari konsumsi makanan tinggi garam dan alkohol di malam hari',
      'Jangan tidur larut malam / begadang kronis',
      'Hindari mengucek kulit bawah mata karena jaringan dermis sangat tipis'
    ],
    redFlags: [
      'Pembengkakan hanya pada satu sisi mata disertai nyeri berdenyut atau warna kemerahan meradang'
    ],
    imageUrl: '/images/conditions/dark-circles.jpg'
  },
  'Eyelid': {
    id: 'eyelid',
    name: 'Kelainan Kelopak Mata (Eyelid / Blefaritis / Bintitan)',
    latinName: 'Blepharitis / Hordeolum / Chalazion',
    icd10: 'H01.0',
    category: 'Palpebra & Kelenjar Meibom',
    description: 'Peradangan kronis atau infeksi fokal pada folikel bulu mata dan kelenjar meibom di sepanjang margin kelopak mata.',
    severity: 'Sedang',
    symptoms: [
      'Benjolan kemerahan yang nyeri pada pangkal bulu mata (bintitan)',
      'Tepian kelopak mata merah, bengkak, berkeropeng, atau bersisik seperti ketombe',
      'Bulu mata rontok atau tumbuh mengarah ke dalam (trikiasis)',
      'Kelopak mata terasa berat atau sulit dibuka di pagi hari'
    ],
    selfCare: [
      {
        title: 'Kompres Hangat Suhu 40°C',
        desc: 'Tempelkan handuk basah hangat selama 5-10 menit 2-3 kali sehari untuk melunakkan minyak kelenjar meibom yang tersumbat.',
        icon: 'waves'
      },
      {
        title: 'Scrub Sampo Bayi / Lid Wipes Khusus',
        desc: 'Bersihkan margin kelopak mata dengan kapas dibasahi sampo bayi lembut yang diencerkan untuk mengangkat biofilm bakteri.',
        icon: 'sanitizer'
      },
      {
        title: 'Pijat Lembut Arah Tepi Kelopak',
        desc: 'Pijat perlahan dari pangkal ke arah tepi bulu mata untuk membantu pengeluaran sekret lemak.',
        icon: 'touch_app'
      }
    ],
    restrictions: [
      'JANGAN PERNAH MEMENCET ATAU MEMECAHKAN BINTITAN: Risiko penyebaran selulitis orbita yang berbahaya',
      'Stop penggunaan riasan mata (maskara/eyeliner) sampai sembuh total',
      'Jangan gunakan lensa kontak saat kelopak sedang meradang aktif'
    ],
    redFlags: [
      'Pembengkakan menyebar ke seluruh pipi atau mata tidak bisa dibuka sama sekali',
      'Disertai demam tinggi atau gangguan gerak bola mata'
    ],
    imageUrl: '/images/conditions/eyelid.jpg'
  },
  'Tidak Terdeteksi': {
    id: 'unclear',
    name: 'Citra Kurang Jelas / Belum Terfokus',
    latinName: 'Imago Ocularis Non Determinata',
    icd10: 'R69',
    category: 'Kalibrasi Citra Belum Optimal',
    description: 'Citra mata yang diambil belum memenuhi ambang batas ketajaman klinis (fokus kurang tajam, pencahayaan kurang merata, atau jarak kamera terlalu jauh).',
    severity: 'Ringan',
    symptoms: [
      'Pencahayaan foto terlalu gelap atau terdapat pantulan kilau silau (glare)',
      'Jarak lensa kamera terlalu jauh dari mata atau sudut pengambilan miring',
      'Area sklera, pupil, atau kelopak mata terhalang sebagian'
    ],
    selfCare: [
      {
        title: 'Dekatkan Kamera 15–25 cm',
        desc: 'Posisikan kamera sejajar tepat di depan mata dalam jarak 15–25 cm agar detail anterior terekam tajam.',
        icon: 'center_focus_strong'
      },
      {
        title: 'Pencahayaan Terang & Merata',
        desc: 'Hadapkan wajah ke sumber cahaya alami atau lampu ruangan yang terang tanpa bayangan pekat pada mata.',
        icon: 'wb_sunny'
      },
      {
        title: 'Buka Mata Rileks & Fokus',
        desc: 'Buka kelopak mata dengan santai dan tahan gerakan mengedip sesaat saat tombol foto ditekan.',
        icon: 'remove_red_eye'
      }
    ],
    restrictions: [
      'Hindari mengambil foto dalam ruangan remang-remang atau melawan backlight',
      'Hindari foto buram akibat tangan goyang saat menjepret kamera HP'
    ],
    redFlags: [
      'Jika mata Anda terasa nyeri menusuk, merah meradang, atau buram mendadak, segera periksa ke dokter spesialis mata (Sp.M)'
    ],
    imageUrl: '/images/conditions/normal.jpg'
  }
};
