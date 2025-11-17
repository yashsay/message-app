# Message App Frontend

Modern React frontend for the Message App, built with **React 19**, **Vite**, and **SCSS**. Features advanced search capabilities, conversation management, real-time summarization, and atmospheric UI design.

## Features

- **Dual Search Modes**: Toggle between keyword and AI-powered semantic search
- **Conversation Management**: Messages grouped by conversation with individual controls
- **Real-time Summarization**: Generate extractive summaries with keyword highlights
- **Modern React 19**: Latest React features with functional components and hooks
- **SCSS Styling**: Modular theming with custom design system
- **Atmospheric UI**: DarkVeil component with immersive visual effects
- **Responsive Design**: Mobile-friendly layout with adaptive components
- **API Integration**: Seamless communication with FastAPI backend
- **Hot Module Replacement**: Lightning-fast development with Vite

---

## Getting Started

### Prerequisites

- **Node.js** (v16 or higher recommended)
- **npm** or **yarn**
- **Backend API** running on port 8000 (see backend README)

### Key Dependencies

- **React 19.1.1**: Latest React with improved performance
- **Vite 7.1.0**: Next-generation frontend tooling
- **Axios 1.11.0**: HTTP client for API communication
- **SASS 1.90.0**: CSS preprocessor for advanced styling
- **OGL 1.0.11**: WebGL library for visual effects

### Installation

1. Navigate to the `frontend` directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   # or
   yarn install
   ```

### Running the Development Server

Start the app in development mode with hot module replacement:

```sh
npm run dev
# or
yarn dev
```

The app will be available at [http://localhost:5173](http://localhost:5173) by default.

**Development Features:**

- Hot module replacement for instant updates
- Automatic browser refresh on file changes
- Source maps for debugging
- Fast refresh for React components

### Building for Production

To build the app for production:

```sh
npm run build
# or
yarn build
```

The output will be in the `dist` folder.

### Preview Production Build

To preview the production build locally:

```sh
npm run preview
# or
yarn preview
```

### Linting

To run ESLint:

```sh
npm run lint
# or
yarn lint
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── MessageList.jsx         # Main message display and search
│   │   ├── MessageList.scss        # Message styling
│   │   ├── DarkVeil/
│   │   │   ├── DarkVeil.jsx       # Atmospheric background effects
│   │   │   └── DarkVeil.css       # Visual effects styling
│   │   └── layout/
│   │       ├── Header.jsx         # Application header
│   │       └── Header.scss        # Header styling
│   ├── styles/
│   │   └── _theme.scss            # Global theme variables
│   ├── assets/
│   │   ├── brain.svg              # AI search icon
│   │   └── react.svg              # React logo
│   ├── App.jsx                    # Main application component
│   ├── App.css                    # Application-wide styles
│   ├── main.jsx                   # React application entry point
│   └── index.css                  # Global CSS reset and base styles
├── public/
│   ├── noise.svg                  # Background texture
│   └── vite.svg                   # Vite logo
├── index.html                     # HTML template
├── package.json                   # Dependencies and scripts
├── vite.config.js                 # Vite configuration
├── eslint.config.js               # ESLint configuration
└── README.md                      # This file
```

## Component Architecture

### MessageList Component

- **Search Interface**: Dual-mode search with toggle between keyword and semantic
- **Conversation Grouping**: Automatic organization by conversation ID
- **Summarization**: Per-conversation summary generation with highlights
- **Real-time Updates**: Dynamic message filtering and display

### DarkVeil Component

- **WebGL Effects**: Atmospheric background using OGL library
- **Performance Optimized**: Efficient rendering with minimal impact
- **Responsive**: Adapts to different screen sizes

### Header Component

- **Navigation**: Application branding and navigation
- **Responsive Design**: Mobile-friendly layout

## Development Notes

### API Integration

- **Base URL**: `http://localhost:8000` (configurable)
- **Endpoints Used**:
  - `GET /api/messages` - Fetch all messages
  - `POST /api/search` - Keyword search
  - `POST /api/semantic-search` - AI-powered search
  - `POST /api/summarize` - Conversation summarization

### Styling System

- **SCSS Variables**: Centralized theming in `src/styles/_theme.scss`
- **Component Styles**: Co-located SCSS files for each component
- **Responsive Design**: Mobile-first approach with breakpoints
- **Dark Theme**: Optimized for dark backgrounds and readability

### Performance

- **Vite HMR**: Instant updates during development
- **Code Splitting**: Automatic optimization for production builds
- **Asset Optimization**: SVG icons and optimized images
- **React 19**: Latest performance improvements and features

### Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **WebGL Support**: Required for DarkVeil visual effects
- **ES6+ Features**: Modern JavaScript syntax and features

## Backend Integration

This frontend requires the Message App backend to be running. See the main project README or `../backend/README.md` for backend setup instructions.

## Troubleshooting

- **API Connection Issues**: Ensure backend is running on port 8000
- **Build Errors**: Clear `node_modules` and reinstall dependencies
- **Styling Issues**: Check SCSS compilation and import paths
- **Performance Issues**: Disable DarkVeil effects if needed

---

For complete project setup and backend integration, see the main project README.
