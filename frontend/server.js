const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = 3000;

/**
 * Express Frontend Server
 * 
 * 1. Proxies /api requests to the FastAPI backend (port 8000)
 * 2. Rewrites path to remove /api prefix
 * 3. Serves static files from the /public directory
 */

// API Proxy Configuration
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api': '', // Remove /api prefix when forwarding to backend
    },
}));

// Serve static assets from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Fallback to index.html for any non-API routes (supporting SPA-like behavior if needed)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 FlightHub Frontend Server running at http://localhost:${PORT}`);
    console.log(`📡 Proxying /api requests to http://localhost:8000`);
});
