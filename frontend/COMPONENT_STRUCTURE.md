# Frontend Component Structure

## Overview

The frontend has been refactored into a clean, modular component architecture with proper separation of concerns.

## Component Architecture

### Layout Components

- `Layout/Layout.jsx` - Main layout wrapper with header and content area
- `Header/Header.jsx` - Application header component

### Message Components

- `MessageList.jsx` - Main container for message functionality
- `ConversationBlock/ConversationBlock.jsx` - Individual conversation container
- `Message/Message.jsx` - Individual message display component
- `SearchBar/SearchBar.jsx` - Search interface component
- `SummarySection/SummarySection.jsx` - Conversation summary display

### Background Components

- `DarkVeil/DarkVeil.jsx` - WebGL-based animated background

## Custom Hooks

- `hooks/useApi.js` - API interaction hooks for messages, search, and summarization

## Key Improvements Made

### 1. Component Separation

- Extracted inline components into separate files
- Created reusable components with proper props
- Organized components in logical folders

### 2. Custom Hooks

- Created `useMessages`, `useSearch`, and `useSummarize` hooks
- Centralized API logic and state management
- Improved error handling and loading states

### 3. PropTypes Validation

- Added PropTypes to all components for better type safety
- Defined clear component interfaces

### 4. Styling Organization

- Component-specific SCSS files
- Consistent naming conventions using BEM methodology
- Proper theme variable usage

### 5. Better Code Organization

- Index files for cleaner imports
- Consistent file naming
- Clear folder structure

## Component Props

### SearchBar

```jsx
<SearchBar
  query={string}
  onQueryChange={function}
  onSearch={function}
  useAI={boolean}
  onToggleAI={function}
/>
```

### ConversationBlock

```jsx
<ConversationBlock
  conversationId={string}
  messages={array}
  summary={object}
  onSummarize={function}
/>
```

### Message

```jsx
<Message message={object} />
```

### SummarySection

```jsx
<SummarySection
  conversationId={string}
  summary={object}
  onSummarize={function}
/>
```

## Usage

Import components from the main index file:

```jsx
import { MessageList, SearchBar, Layout } from "./components";
```

Or import hooks:

```jsx
import { useMessages, useSearch } from "./hooks";
```
