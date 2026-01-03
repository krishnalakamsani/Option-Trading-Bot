# Trading Bot Dashboard - Frontend Application

## Overview

A beautiful, modern web dashboard to manage and monitor your Index Options Trading Bot. Built with React and Tailwind CSS.

## Features

### 1. Dashboard
- Real-time bot status monitoring
- Today's P&L display
- Performance metrics (win rate, avg win/loss)
- Live configuration overview
- Trading statistics

### 2. Configuration
- Easy-to-use interface for all bot settings
- Dhan API credentials management
- Trading mode selection (Paper/Live)
- Risk management controls
- SuperTrend strategy parameters
- Real-time validation

### 3. Trades
- Complete trade history
- Real-time performance analytics
- P&L tracking
- Win/loss statistics
- Detailed trade information (time, symbol, price, quantity)

### 4. Logs
- Real-time log streaming
- Color-coded log levels (Error, Warning, Info, Signal, Trade)
- Auto-refresh capability
- Last 200 log entries
- Easy filtering and search

## Tech Stack

- **Framework**: React 18
- **UI Library**: Shadcn/UI
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Notifications**: Sonner
- **HTTP Client**: Axios
- **Routing**: React Router DOM

## Pages

### Dashboard (`/`)
- Overview of bot performance
- Quick stats cards
- Configuration summary
- Bot status indicator

### Configuration (`/config`)
- Edit all bot settings
- Save changes
- Real-time updates
- Input validation

### Trades (`/trades`)
- Trade history table
- Performance metrics
- P&L visualization
- Trade details

### Logs (`/logs`)
- Real-time log viewer
- Auto-refresh toggle
- Color-coded entries
- Log level legend

## API Endpoints Used

### Bot Management
- `GET /api/bot/status` - Get bot status
- `POST /api/bot/start` - Start the bot
- `POST /api/bot/stop` - Stop the bot

### Configuration
- `GET /api/bot/config` - Get current config
- `POST /api/bot/config` - Update config

### Data
- `GET /api/bot/trades` - Get today's trades
- `GET /api/bot/logs?lines=200` - Get recent logs
- `GET /api/bot/performance` - Get performance metrics

## Quick Start

### Prerequisites
- Backend server running on port 8001
- Node.js 16+ installed
- Yarn package manager

### Installation

```bash
cd /app/frontend
yarn install
```

### Development

```bash
yarn start
```

Runs on http://localhost:3000

### Build

```bash
yarn build
```

Creates optimized production build in `build/` folder.

## Environment Variables

Create `.env` file:

```bash
REACT_APP_BACKEND_URL=http://your-backend-url
```

For local development:
```bash
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Features Explained

### Start/Stop Bot
Click the button in the header to start or stop the trading bot. Status indicator shows if bot is running (green pulse) or stopped (red).

### Real-time Updates
- Dashboard refreshes every 5 seconds
- Trades page updates every 5 seconds
- Logs page updates every 3 seconds (when auto-refresh is ON)

### Configuration Changes
1. Edit settings in Configuration page
2. Click "Save Changes"
3. Stop the bot
4. Start the bot again for changes to take effect

### Monitoring
- Green pulsing dot = Bot running
- Red dot = Bot stopped
- Real-time P&L updates
- Live trade notifications

## UI Components

Built with Shadcn/UI components:
- `Button` - Action buttons
- `Card` - Content containers
- `Input` - Form inputs
- `Select` - Dropdowns
- `Table` - Data tables
- `Badge` - Status indicators
- `Label` - Form labels

## Design Features

- Clean, modern interface
- Responsive design (mobile-friendly)
- Smooth animations
- Color-coded status indicators
- Easy navigation sidebar
- Professional color scheme
- Inter font for readability

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Cannot connect to backend
- Check if backend is running: `sudo supervisorctl status backend`
- Verify `REACT_APP_BACKEND_URL` in `.env`
- Check browser console for errors

### Changes not reflected
- Clear browser cache
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Restart frontend: `sudo supervisorctl restart frontend`

### API errors
- Check backend logs: `tail -f /var/log/supervisor/backend.err.log`
- Verify bot directory exists: `/app/index_options_bot`
- Check file permissions

## Development Tips

### Adding New Pages
1. Create page in `src/pages/YourPage.jsx`
2. Add route in `src/App.js`
3. Add navigation item in `src/components/Layout.jsx`

### Styling
- Use Tailwind CSS classes
- Follow existing component patterns
- Use Shadcn/UI components when possible
- Maintain color consistency

### API Calls
- Always use `${API}` prefix
- Handle errors with toast notifications
- Add loading states
- Use async/await

## Security Notes

- API tokens are masked in the UI
- HTTPS recommended for production
- CORS configured in backend
- Input validation on both frontend and backend

## Performance

- Lazy loading for pages
- Optimized re-renders
- Efficient state management
- Minimal bundle size

## Future Enhancements

- [ ] Charts and graphs for P&L
- [ ] Export trades to CSV
- [ ] Advanced filtering
- [ ] Dark mode toggle
- [ ] Push notifications
- [ ] Strategy backtesting UI
- [ ] Multiple bot management
- [ ] User authentication

## Support

For issues or questions:
1. Check browser console
2. Review backend logs
3. Verify API connectivity
4. Check configuration settings

---

**Version**: 1.0.0  
**Last Updated**: January 3, 2026  
**Built with**: React + Tailwind CSS + Shadcn/UI
