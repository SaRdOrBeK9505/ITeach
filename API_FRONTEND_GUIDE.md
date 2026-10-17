# 🚀 ITeach REST API – Frontend Developer Guide

Ushbu qo'llanma **Frontend jamoasi** (Asosiy sayt / Landing va Admin Dashboard) uchun tayyorlangan. Unda har bir endpointning maqsadi, qachon va qayerda ishlatilishi, kerakli parametrlar hamda so'rov/javob namunalari keltirilgan.

---

## 📌 Asosiy ma'lumotlar (General Info)

* **Base URL (Local):** `http://127.0.0.1:8000`
* **Base URL (PythonAnywhere):** `https://<sizning_username>.pythonanywhere.com`
* **Swagger interaktiv hujjat:** `BASE_URL/` (Swagger UI) yoki `BASE_URL/api/redoc/`
* **JSON Schema:** `BASE_URL/api/schema.json`
* **Format:** Barcha so'rov va javoblar `application/json` formatida bo'ladi (Fayl yuklashda esa `multipart/form-data`).

### 🔐 Autentifikatsiya (Authorization Header)
Public endpointlar uchun hech qanday token kerak emas.
Admin / CRM endpointlari uchun JWT token talab qilinadi:
```http
Authorization: Bearer <access_token>
```

---

## 1. 🌐 Public Endpointlar (Asosiy Landing Sayt uchun)

Ushbu endpointlar `https://iteachh.vercel.app` sayti uchun mo'ljallangan va ochiq (hech qanday token talab qilinmaydi).

### ⚡ Super Endpoint: Butun Bosh Sahifa (All-in-One)
Bosh sahifani tez yuklash va 10 ta alohida so'rov yubormaslik uchun barcha bloklar ma'lumotini 1 ta so'rovda olish mumkin:

* **URL:** `GET /api/landing/`
* **Qachon ishlatiladi:** Asosiy sahifa (Home Page `index.tsx`/`page.tsx`) birinchi yuklanganda (`getServerSideProps` yoki `useEffect`).
* **Javob (Response):**
```json
{
  "settings": { "site_name": "ITeach", "phone_1": "+998 90 123 45 67", ... },
  "hero": { "title": "Kelajak kasblarini biz bilan o'rganing", ... },
  "hero_slides": [ ... ],
  "statistics": [ { "title": "Bitiruvchilar", "value": 1500, "suffix": "+" } ],
  "about": { ... },
  "courses": [ ... ],
  "student_results": [ ... ],
  "learning_process": [ ... ],
  "mentors": [ ... ],
  "partners": [ ... ],
  "graduates": [ ... ],
  "testimonials": [ ... ],
  "faqs": [ ... ],
  "latest_posts": [ ... ]
}
```

---

### 📚 Kurslar va Kategoriyalar (Courses)

#### 1. Barcha faol kurslar ro'yxati
* **URL:** `GET /api/courses/`
* **Qachon ishlatiladi:** Kurslar sahifasi yoki kurslar bo'limida barcha kurslarni ko'rsatishda.
* **Query parametrlar:**
  * `?category=<category_id>` — Ma'lum bir yo'nalish bo'yicha filtrlash (masalan: `?category=2`).
  * `?level=beginner|intermediate|advanced` — Qiyinlik darajasi bo'yicha.
  * `?is_popular=true` — Faqat ommabop kurslarni olish.
  * `?search=python` — Kurs nomi bo'yicha qidiruv.
  * `?ordering=price` yoki `?ordering=-price` — Narx bo'yicha saralash.

#### 2. Kursning to'liq ma'lumotlari (Batafsil sahifa)
* **URL:** `GET /api/courses/<slug>/` (masalan: `/api/courses/frontend-dasturlash/`)
* **Qachon ishlatiladi:** Foydalanuvchi ma'lum bir kurs ustiga bosib, uning ichki sahifasiga (`/courses/[slug]`) o'tganda.
* **Javobda:** Kurs ta'rifi, mentori, xususiyatlari (`features`), o'tiladigan mavzular va narxi to'liq keladi.

#### 3. Kurs kategoriyalari (Tablar uchun)
* **URL:** `GET /api/course-categories/`
* **Qachon ishlatiladi:** Kurslar bo'limidagi filtrlash tugmalari (All, Dasturlash, Dizayn, Marketing) tablarini chiqarishda.

---

### 👨‍🏫 Mentorlar (O'qituvchilar)

* **URL:** `GET /api/mentors/`
* **Qachon ishlatiladi:** "Bizning jamoa / Mentorlar" blokida o'qituvchilar karuseli yoki ro'yxatini ko'rsatishda.
* **Bitta mentorni ko'rish:** `GET /api/mentors/<id>/` (Mentor haqida alohida sahifa bo'lsa).

---

### 🎬 Natijalar, Reels va O'quv Jarayoni

#### 1. O'quvchilar natijalari va video lavhalar (Reels)
* **URL:** `GET /api/results/`
* **Qachon ishlatiladi:** Saytdagi "Natijalar" yoki "O'quvchilarimiz loyihalari / Reels" bo'limida (Instagram/YouTube formatidagi qisqa videolarni ko'rsatishda).

#### 2. O'quv jarayoni bosqichlari (How it works)
* **URL:** `GET /api/learning-process/`
* **Qachon ishlatiladi:** "Ta'lim qanday amalga oshiriladi?" 1-qadam, 2-qadam, 3-qadam ko'rinishidagi blok uchun.

#### 3. Bitiruvchilar qayerda ishlaydi (Graduates)
* **URL:** `GET /api/graduates/`
* **Qachon ishlatiladi:** Bitiruvchilarning ish joylari, lavozimlari va maoshlari keltirilgan muvaffaqiyat hikoyalari blokida.

#### 4. Hamkorlar (Partners)
* **URL:** `GET /api/partners/`
* **Qachon ishlatiladi:** Markaz bilan hamkor IT kompaniyalar logotiplari karuselida.

#### 5. Izohlar / Fikrlar (Testimonials)
* **URL:** `GET /api/testimonials/`
* **Filtr:** `?course=<course_id>` (Muayyan kurs haqidagi fikrlar).

#### 6. Ko'p beriladigan savollar (FAQ)
* **URL:** `GET /api/faq/`
* **Qachon ishlatiladi:** Accordion ko'rinishidagi savol-javoblar blokida.

---

### 📰 Blog / Yangiliklar

* **URL:** `GET /api/blog/` — Barcha nashr qilingan maqolalar (Paginatsiya bilan).
  * `?category=<category_id>` — Kategoriya bo'yicha.
  * `?search=react` — Maqolalar ichidan qidirish.
* **URL:** `GET /api/blog/<slug>/` — Bitta maqolaning to'liq matni va rasmlari.
* **URL:** `GET /api/blog/categories/` — Blog kategoriyalari ro'yxati.

---

### 📩 Formalar (Ariza va Aloqa xabarlari)

#### 1. Kursga yozilish arizasi (Lead form)
* **URL:** `POST /api/apply/`
* **Qachon ishlatiladi:** Modal oynadagi "Kursga yozilish", "Bepul konsultatsiya olish" yoki "Ariza qoldirish" tugmasi bosilganda.
* **Request Body:**
```json
{
  "full_name": "Azizbek Rahimov",
  "phone": "+998901234567",
  "course": 2,          // ixtiyoriy (kurs ID si)
  "message": "Kechki guruhga yozilmoqchiman" // ixtiyoriy
}
```
* **Status:** `201 Created`

#### 2. Biz bilan bog'lanish (Contact Message)
* **URL:** `POST /api/contact/`
* **Qachon ishlatiladi:** Saytning "Aloqa" / "Contact Us" sahifasidagi xabar yuborish formasida.
* **Request Body:**
```json
{
  "full_name": "Jamshid Qodirov",
  "email": "jamshid@example.com",
  "phone": "+998991112233",
  "subject": "Hamkorlik masalasida",
  "message": "Biz kompaniyamiz xodimlari uchun korporativ ta'lim olmoqchimiz..."
}
```
* **Status:** `201 Created`

---

## 2. 🔐 Admin va CRM Endpointlari (Dashboard uchun)

Ushbu endpointlar `https://admin-pi-two-47.vercel.app` (Admin portal) uchun mo'ljallangan.

### 🔑 Autentifikatsiya (Accounts)

#### 1. Admin login (JWT olish)
* **URL:** `POST /api/auth/login/`
* **Body:**
```json
{
  "username": "admin",  // yoki email
  "password": "sizning_parolingiz"
}
```
* **Javob:**
```json
{
  "access": "eyJhbGciOi...",
  "refresh": "eyJhbGciOi...",
  "role": "superadmin", // yoki "admin", "mentor", "student"
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@iteach.uz",
    "full_name": "Sardorbek Admin",
    "role": "superadmin",
    "role_display": "Bosh Administrator",
    "phone": "+998901234567",
    "is_staff": true,
    "is_superuser": true
  }
}
```

> **Eslatma:** JWT `access` token payload ichida ham `role`, `username`, `is_staff` claimlari mavjud.

#### 2. Tokenni yangilash (Refresh)
* **URL:** `POST /api/auth/refresh/` yoki `POST /api/auth/token/refresh/`
* **Body:** `{ "refresh": "<refresh_token>" }`
* **Javob:**
```json
{
  "access": "<yangi_access_token>",
  "refresh": "<yangi_refresh_token>",
  "role": "superadmin"
}
```

#### 3. Admin profili
* **URL:** `GET /api/auth/me/` — Hozir tizimga kirgan admin ma'lumotlari.
* **URL:** `PATCH /api/auth/me/` — Ism, familiya yoki emailni o'zgartirish.
* **URL:** `POST /api/auth/change-password/` — Parolni yangilash (`old_password`, `new_password`, `confirm_password`).

---

### 📊 Dashboard Asosiy Sahifasi (KPI & Analytics)

#### 1. Umumiy hisobot kartalari va oxirgi jadvallar
* **URL:** `GET /api/admin/dashboard/`
* **Qachon ishlatiladi:** Admin panelga kirgandagi asosiy Dashboard sahifasida.
* **Javob:**
  * `metrics`: Kurslar soni, faol o'quvchilar, mentorlar, arizalar soni, yangi ko'rilmagan arizalar soni, o'qilmagan xabarlar.
  * `recent_students`: Oxirgi ro'yxatga olingan 10 ta o'quvchi.
  * `courses`: Faol kurslar ro'yxati.
  * `recent_applications`: Oxirgi kelib tushgan 10 ta ariza.

#### 2. Grafik va Diagrammalar (Charts & Analytics)
* **URL:** `GET /api/admin/dashboard/analytics/`
* **Qachon ishlatiladi:** Statistika va grafiklar sahifasida (Chart.js / Recharts uchun).
* **Javob:**
  * `course_distribution`: Har bir kursda nechtadan o'quvchi o'qiyotgani (Pie / Bar chart uchun).
  * `applications_breakdown`: Arizalar holati (`new`, `called`, `enrolled`, `rejected`).

---

### 👨‍🎓 O'quvchilar boshqaruvi (Students CRM)

* **URL:** `GET /api/admin/students/` — Barcha o'quvchilar ro'yxati (Paginatsiya bilan).
  * `?status=Faol|Tugatgan|Muzlatilgan|Ketgan` — Holati bo'yicha filter.
  * `?course=<course_id>` — Kurs bo'yicha filter.
  * `?search=Alisher` — Ismi, telefoni yoki vaqti bo'yicha qidirish.
  * `?ordering=-created_at` — Yangi qo'shilganlar bo'yicha tartiblash.
* **URL:** `POST /api/admin/students/` — Yangi o'quvchi qo'shish.
  * Body: `full_name`, `phone`, `email`, `course` (id), `status`, `enrolled_date`, `lesson_time`, `monthly_payment`, `notes`.
* **URL:** `GET /api/admin/students/<id>/` — Bitta o'quvchi profilini to'liq ko'rish.
* **URL:** `PUT/PATCH /api/admin/students/<id>/` — O'quvchi ma'lumotlarini tahrirlash.
* **URL:** `DELETE /api/admin/students/<id>/` — O'quvchini o'chirish.

---

### 📋 Arizalar (Leads / Applications) Boshqaruvi

* **URL:** `GET /api/admin/applications/` — Saytdan kelgan barcha arizalar.
  * `?status=new|called|enrolled|rejected` — Status bo'yicha filter.
  * `?search=telefon` — Qidiruv.
* **URL:** `GET /api/admin/applications/<id>/` — Ariza tafsilotlari.
* **URL:** `PATCH /api/admin/applications/<id>/` — Arizaning statusini yoki ichki izohlarini yangilash (masalan: `status: "called"` yoki `admin_notes: "Telefon ko'tarmadi"`).

#### ⚡ Arizani bir bosishda O'quvchiga aylantirish (Convert to Student)
* **URL:** `POST /api/admin/applications/<id>/convert-to-student/`
* **Qachon ishlatiladi:** Admin arizachi bilan gaplashib uni o'quvchilar safiga qabul qilganda.
* **Natija:** Ushbu ariza statusi avtomatik `enrolled` bo'ladi va Students jadvalida yangi `Faol` o'quvchi avtomatik yaratiladi!

---

### 🛠 Kontent Boshqaruvi (CRUD bo'limlari)

Admin quyidagi barcha bo'limlarni to'liq boshqara oladi (GET, POST, PUT/PATCH, DELETE):

| Bo'lim | Admin URL | Qo'shimcha imkoniyat |
| :--- | :--- | :--- |
| **Kurslar** | `/api/admin/courses/` | Kurs rasmi, narxi, darajasi, mentorini belgilash |
| **Kurs xususiyatlari** | `/api/admin/courses/<course_id>/features/` | Kurs ichidagi afzalliklar ro'yxati |
| **Kategoriyalar** | `/api/admin/course-categories/` | Yangi yo'nalishlar ochish |
| **Mentorlar** | `/api/admin/mentors/` | O'qituvchi rasmi, tajribasi, ijtimoiy tarmoqlari |
| **Natijalar/Reels** | `/api/admin/results/` | Video linki, o'quvchi natijasi |
| **O'quv jarayoni** | `/api/admin/learning-process/` | Bosqichlar va tartib raqamlari |
| **Blog maqolalari** | `/api/admin/blog/` | Rasm, to'liq maqola matni, kategoriyasi |
| **FAQ** | `/api/admin/faq/` | Savollar va javoblar |
| **Fikrlar** | `/api/admin/testimonials/` | O'quvchilar fikrlari |
| **Aloqa xabarlari** | `/api/admin/contacts/` | Kelgan xabarlar (`is_read: true` qilish) |
| **Sayt sozlamalari** | `/api/admin/settings/` | Telefonlar, manzil, logotip, ijtimoiy tarmoqlar |

---

## 💡 Frontend Dasturchilari uchun Maslahatlar (Tips)

1. **Rasm URL lari:** Backend media fayllar uchun to'liq URL qaytaradi (masalan: `http://127.0.0.1:8000/media/courses/react.png`). Next.js `next/image` komponentida ishlaganda `next.config.js` ga API domeningizni `remotePatterns` ga qo'shib qo'ying:
   ```javascript
   // next.config.js
   images: {
     remotePatterns: [
       { protocol: 'https', hostname: '**.pythonanywhere.com' },
       { protocol: 'http', hostname: '127.0.0.1' },
     ],
   }
   ```
2. **Paginatsiya:** Ro'yxat qaytaradigan GET endpointlar `count`, `next`, `previous`, `results` ko'rinishida sahifalangan javob beradi. Har bir sahifada standart 20 tadan ma'lumot bo'ladi.
3. **CORS:** Barcha domenlar (`localhost:3000`, `localhost:5173`, `iteachh.vercel.app`, `admin-pi-two-47.vercel.app`) uchun CORS ruxsat berilgan.

---
*Savollar yoki qo'shimcha endpointlar kerak bo'lsa, backend jamoasiga murojaat qiling.*
