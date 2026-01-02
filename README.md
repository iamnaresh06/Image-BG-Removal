# Image Background Removal Tool

A powerful web-based application built with Django that automatically removes backgrounds from images using advanced AI algorithms (`rembg`). This tool provides a simple, user-friendly interface for uploading images, processing them with high precision, and downloading the results in various formats.

## 🚀 Features

- **Automated Background Removal**: Instant background removal using the `rembg` library (U-2-Net).
- **Edge Refinement**: Option for "Refine Edges" (Alpha Matting) to handle complex details like hair or fur.
- **Format Conversion**: Download processed images in **PNG**, **JPG**, or **WebP** formats.
- **Custom Backgrounds**: Option to add solid background colors to the processed image before downloading.
- **Side-by-Side Comparison**: View original and processed images instantly.
- **Responsive Design**: Clean and modern UI that works on desktop and mobile.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Image Processing**: `rembg`, `Pillow` (PIL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (Default Django setup)

## 📂 File Structure

```
Image_BgRemoval_Tool/
├── bg_removal/                 # Project configuration directory
│   ├── settings.py             # Main Django settings
│   ├── urls.py                 # Project-level URL routing
│   └── wsgi.py/asgi.py         # Server entry points
├── remover/                    # Main application directory
│   ├── migrations/             # Database migrations
│   ├── static/                 # Static files (CSS, Images)
│   ├── templates/              # HTML Templates (index.html, result.html)
│   ├── urls.py                 # App-level URL routing
│   ├── views.py                # Core application logic & image processing
│   └── apps.py                 # App configuration
├── media/                      # Directory for media files
│   ├── uploaded_images/        # Original user uploads
│   └── processed_images/       # Background-removed results
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── db.sqlite3                  # SQLite database
```

## ⚙️ Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.8+ installed
- `pip` (Python package manager)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/iamnaresh06/Image-BG-Removal.git
    cd Image_BgRemoval_Tool
    ```

2.  **Create a Virtual Environment** (Recommended)
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time you run the tool, `rembg` will download the necessary AI models (~170MB). This happens automatically.*

4.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Start the Development Server**
    ```bash
    python manage.py runserver
    ```

6.  **Access the App**
    Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📖 Usage

1.  **Upload Info**: Click "Choose File" to select an image (`.jpg`, `.png`, `.jpeg`).
2.  **Refine Edges**: Check "Refine Edges" if your image has complex details (like hair).
3.  **Remove**: Click "Remove Background".
4.  **Edit & Download**:
    - Select a new background color if desired.
    - Choose a file format (`PNG` for transparency, others for smaller size).
    - Click "Download" to save the result.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

## 📬 Contact

**Naresh Reddy**  
*Full Stack Developer*

- **Email**: [06.nareshreddy@gmail.com](mailto:06.nareshreddy@gmail.com)
- **LinkedIn**: [iamnaresh06](https://www.linkedin.com/in/iamnaresh06/)
- **GitHub**: [iamnaresh06](https://github.com/iamnaresh06)
- **Portfolio**: [reddynaresh.netlify.app](https://reddynaresh.netlify.app/)
- **LeetCode**: [iamnaresh_06](https://leetcode.com/u/iamnaresh_06/)
