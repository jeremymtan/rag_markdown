# Tako RAG Chat - Next.js App

A modern React + Next.js chat interface for the Tako RAG system.

## Prerequisites

- Node.js 18+ 
- The FastAPI backend running on http://localhost:8000

## Setup

1. Install dependencies:
```bash
cd web
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open http://localhost:3000 in your browser

## Features

- Clean, modern chat interface built with React
- Real-time streaming responses
- Source attribution display
- Responsive design with Tailwind CSS
- Loading states and error handling
- Automatic scrolling to latest messages

## Development

The app uses:
- Next.js 14 with App Router
- React 18
- TypeScript
- Tailwind CSS for styling
- API proxy to avoid CORS issues

## Production

To build for production:
```bash
npm run build
npm start
```