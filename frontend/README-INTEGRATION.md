# Gazman Clone - AI Try-On Integration

This project integrates a React frontend with a Python Flask backend to provide AI-powered virtual try-on functionality for fashion e-commerce.

## 🚀 Quick Start

### Option 1: Use the startup script (Recommended)
```bash
./start-dev.sh
```

### Option 2: Start manually

**Terminal 1 - Backend:**
```bash
cd headswapper
source venv/bin/activate
python3 analyze_user_image.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

## 📁 Project Structure

```
gazman-product-page/
├── src/
│   ├── components/
│   │   └── TryOnModal.tsx          # AI Try-On modal component
│   ├── services/
│   │   └── api.ts                  # API service for backend communication
│   └── App.tsx                     # Main React app with Try-On integration
├── headswapper/
│   ├── analyze_user_image.py       # Flask backend with AI analysis
│   ├── image_gen/                  # Image generation system
│   └── public/images/bodytypes/    # Pre-generated reference images
└── start-dev.sh                    # Development startup script
```

## 🔧 Backend API Endpoints

### 1. Image Analysis
- **URL**: `POST /api/analyze-user-image`
- **Purpose**: Analyzes uploaded user image to determine body type and skin color
- **Input**: Image file (max 10MB)
- **Output**: JSON with gender, body_type, and skin_color

### 2. Head Swap
- **URL**: `POST /api/swap-head`
- **Purpose**: Performs AI head swap with user image and reference model
- **Input**: Image file + optional reference image path
- **Output**: Base64 encoded result image

### 3. Image Serving
- **URL**: `GET /images/<path>`
- **Purpose**: Serves pre-generated reference images

## 🎨 Frontend Features

### Try-On Modal
- **3-Step Process**:
  1. **Upload**: User uploads their photo
  2. **Analysis**: AI analyzes body type and skin color
  3. **Result**: Shows try-on result with AI head swap

### Integration Points
- **Color Selection**: Automatically uses selected product color
- **Reference Images**: Dynamically loads correct body type/skin color combination
- **Error Handling**: Graceful error handling with user-friendly messages

## 🎯 How It Works

1. **User clicks "Try-On with AI"** on product page
2. **Modal opens** with upload interface
3. **User uploads photo** (validated for type and size)
4. **Backend analyzes** image using OpenAI GPT-4o Vision
5. **System finds matching reference** image based on analysis
6. **AI head swap** performed using external HeadSwapper API
7. **Result displayed** showing user in the selected product

## 🔑 Key Features

### ✅ Body Types Supported
- slim, average, athletic, muscular, stocky, dadbod, overweight

### ✅ Skin Colors Supported
- fair-light, olive, brown, dark-brown

### ✅ Product Colors
- Arctic Fox (currently available)
- Black, Heather (ready for future expansion)

### ✅ AI Analysis
- Automatic body type detection
- Skin color classification
- Gender detection
- Smart fallback system

## 🛠️ Development

### Backend Dependencies
```bash
cd headswapper
pip install -r requirements.txt
```

### Frontend Dependencies
```bash
npm install
```

### Environment Variables
Create `.env` file in `headswapper/` directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚨 Important Notes

1. **Backend Port**: Flask server runs on port 5003
2. **Frontend Port**: React app runs on port 5173
3. **CORS**: Configured for localhost development
4. **File Size**: Maximum 10MB for uploaded images
5. **Image Types**: Supports PNG, JPG, JPEG, GIF, BMP, WebP

## 🔄 API Flow

```
Frontend → Upload Image → Backend Analysis → Find Reference → Head Swap → Display Result
    ↓              ↓              ↓              ↓              ↓              ↓
Try-On Modal → Flask API → OpenAI GPT-4o → Reference Image → HeadSwapper API → Result Image
```

## 🎉 Success!

The integration is complete and ready for testing! The system provides a seamless AI-powered try-on experience for your fashion e-commerce platform. 