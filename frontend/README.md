# JD Sports Frontend

A modern React-based frontend for JD Sports with AI-powered virtual try-on functionality.

## Features

- 🛍️ **Product Catalog**: Browse JD Sports products with detailed information
- 🤖 **AI Try-On**: Upload your photo and see how products look on you
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- ⚡ **Fast Performance**: Built with Next.js 15 and optimized for speed

## Tech Stack

- **Framework**: Next.js 15 with React 18
- **Styling**: Tailwind CSS with custom components
- **UI Components**: Radix UI primitives with custom styling
- **Icons**: Lucide React
- **TypeScript**: Full type safety
- **API**: RESTful API integration with backend services

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm, yarn, or bun

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── ui/            # Reusable UI components
│   ├── Header.tsx     # Site header
│   ├── ProductPage.tsx # Product details page
│   └── TryOnModal.tsx # AI try-on modal
├── services/          # API services
│   └── api.ts         # Backend API integration
└── lib/               # Utility functions
    └── utils.ts       # Common utilities
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Environment Variables

Create a `.env.local` file with:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:5003
```

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test your changes thoroughly
4. Update documentation as needed
