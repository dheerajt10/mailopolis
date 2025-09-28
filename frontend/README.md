# Mailopolis Frontend - Gaming Interface

An immersive, cyberpunk-styled frontend for the Mailopolis adversarial sustainability game. Built with React, featuring real-time updates, stunning visualizations, and advanced gaming UI components.

## 🎮 Features

### Core Game Interface
- **Real-time Dashboard** - Live sustainability metrics and department performance
- **AgentMail System** - Secure communication hub with Mayor and city departments
- **Blockchain Explorer** - Transaction analysis and corruption detection
- **Policy Creator** - Interactive policy crafting with AI suggestions
- **Bad Actor Intelligence** - Advanced threat monitoring and analysis

### Visual Excellence
- **Cyberpunk Aesthetic** - Neon colors, glowing effects, and futuristic UI
- **Smooth Animations** - Framer Motion powered transitions and interactions
- **Data Visualizations** - Charts, meters, and real-time graphs
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile

### Advanced Features
- **WebSocket Integration** - Real-time game state updates
- **AI-Powered Suggestions** - Smart policy recommendations
- **Blockchain Analytics** - Transaction pattern recognition
- **Threat Assessment** - Bad actor behavior analysis

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend server running on port 8000

### Installation

```bash
# Clone and navigate to frontend
cd mailopolis/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Build for Production

```bash
# Create optimized build
npm run build

# Preview production build
npm run preview
```

## 🎨 Tech Stack

### Core Framework
- **React 18** - Modern React with hooks and context
- **Vite** - Lightning-fast build tool and dev server
- **React Router** - Client-side routing

### Styling & Animation
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and transitions
- **Custom CSS** - Cyberpunk theme and gaming effects

### Data & Communication
- **Axios** - HTTP client for API calls  
- **Socket.io Client** - Real-time WebSocket communication
- **React Context** - Global state management

### Visualizations
- **Chart.js + React-Chartjs-2** - Interactive charts and graphs
- **Recharts** - Composed chart components
- **Custom Components** - Specialized game visualizations

### UI Components
- **Lucide React** - Beautiful, customizable icons
- **React Hot Toast** - Elegant notifications
- **Custom Gaming UI** - Specialized components for game interface

## 🏗️ Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # React components
│   │   ├── GameDashboard.jsx      # Main game overview
│   │   ├── AgentMail.jsx          # Communication hub
│   │   ├── BlockchainExplorer.jsx # Transaction analysis
│   │   ├── PolicyCreator.jsx      # Policy crafting interface
│   │   ├── BadActorIntel.jsx      # Threat monitoring
│   │   ├── Navigation.jsx         # App navigation
│   │   ├── HUD.jsx               # Heads-up display
│   │   └── ...                   # Supporting components
│   ├── context/          # React context providers
│   │   └── GameContext.jsx       # Global game state
│   ├── services/         # API and WebSocket services
│   │   ├── GameService.js        # Backend API calls
│   │   └── WebSocketService.js   # Real-time updates
│   ├── App.jsx           # Main application component
│   ├── main.jsx          # Application entry point
│   └── index.css         # Global styles and theme
├── index.html            # HTML template
├── package.json          # Dependencies and scripts
├── tailwind.config.js    # Tailwind configuration
├── vite.config.js        # Vite build configuration
└── README.md            # This file
```

## 🎮 Game Interface Guide

### Dashboard
- **Sustainability Meter** - Main city health indicator
- **Department Grid** - Individual department performance
- **Quick Stats** - Mayor trust, bad actor influence, rounds remaining
- **Trend Charts** - Historical performance data
- **Real-time Alerts** - Critical notifications and recommendations

### AgentMail
- **Inbox Management** - Messages from Mayor, departments, and AI systems
- **Priority Filtering** - Sort by urgency and type
- **Secure Communication** - Encrypted message system
- **Real-time Notifications** - Instant message alerts

### Policy Creator
- **Department Selection** - Choose target for your policies
- **AI Suggestions** - Smart recommendations based on game state
- **Template Library** - Pre-built policy frameworks
- **Impact Assessment** - Predict policy effectiveness

### Blockchain Explorer
- **Transaction Monitoring** - Real-time blockchain analysis
- **Corruption Detection** - AI-powered suspicious activity alerts
- **Pattern Recognition** - Identify bad actor behaviors
- **Evidence Collection** - Build cases against adversaries

### Bad Actor Intelligence
- **Threat Assessment** - Monitor adversary activities
- **Behavior Prediction** - AI forecasts of enemy moves
- **Weakness Analysis** - Find opportunities to counter
- **Strategic Recommendations** - Optimal response tactics

## 🎨 Design System

### Color Palette
- **Cyber Blue** - `#00d4ff` - Primary actions and trust
- **Cyber Green** - `#00ff88` - Success and sustainability
- **Cyber Red** - `#ff0055` - Threats and critical alerts
- **Cyber Yellow** - `#ffff00` - Warnings and energy
- **Cyber Purple** - `#8b5cf6` - Communication and secondary actions

### Typography
- **Orbitron** - Headings and cyber text elements
- **Rajdhani** - Body text and UI elements

### Effects
- **Neon Glows** - Attention-grabbing highlights
- **Data Streams** - Matrix-like background animations
- **Pulse Effects** - Live data indicators
- **Circuit Patterns** - Cyberpunk background textures

## 🔧 Development

### Environment Setup

```bash
# Development with hot reload
npm run dev

# Type checking (if using TypeScript)
npm run type-check

# Linting
npm run lint

# Build optimization analysis
npm run build -- --analyze
```

### Customization

#### Adding New Components
1. Create component in `src/components/`
2. Add route in `App.jsx`
3. Update navigation in `Navigation.jsx`
4. Add to context if needed

#### Styling Guidelines
- Use Tailwind utility classes first
- Create custom CSS for complex animations
- Follow cyberpunk color scheme
- Maintain responsive design patterns

#### API Integration
- Add new endpoints to `GameService.js`
- Handle real-time updates in `WebSocketService.js`
- Update context for global state changes

## 🌟 Advanced Features

### Real-time Updates
The frontend automatically syncs with the backend through WebSocket connections:

```javascript
// Subscribe to game updates
WebSocketService.on('game_update', (data) => {
  // Update local state
})

// Send player actions
WebSocketService.send('player_action', {
  type: 'submit_proposal',
  data: proposalData
})
```

### State Management
Global game state is managed through React Context:

```javascript
const { 
  sustainabilityIndex, 
  departments, 
  submitProposal 
} = useGame()
```

### Animation System
Smooth animations powered by Framer Motion:

```javascript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

## 🚀 Deployment

### Production Build
```bash
# Create optimized build
npm run build

# The build files will be in the `dist` directory
# Deploy these files to your web server
```

### Environment Variables
Create `.env` file for configuration:

```env
VITE_API_BASE_URL=https://your-backend-url.com
VITE_WS_URL=wss://your-websocket-url.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Use functional components with hooks
- Follow React best practices
- Maintain consistent naming conventions
- Write clear, self-documenting code
- Add comments for complex logic

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🎯 Performance

- **Lazy Loading** - Components loaded on demand
- **Code Splitting** - Optimized bundle sizes
- **Memoization** - Prevent unnecessary re-renders
- **Efficient Updates** - Minimal DOM manipulation

## 🛡️ Security

- **Input Validation** - All user inputs sanitized
- **Secure Communication** - HTTPS and WSS protocols
- **Data Protection** - No sensitive data in localStorage
- **CORS Configuration** - Proper cross-origin setup

---

Built with ❤️ for the MHacks hackathon. Experience the future of city sustainability gaming!