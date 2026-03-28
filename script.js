// ============================================
// Main JavaScript for CV2Desk
// ============================================

// Configuration
const API_BASE = 'http://localhost:5000/api';
const STORAGE_KEY = 'cv2desk';

// Authentication state
let isAuthenticated = false;
let currentUser = null;

// Dark Mode Toggle
const themeToggle = document.getElementById('themeToggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

// Initialize theme from localStorage
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 
                      (prefersDark.matches ? 'dark' : 'light');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

themeToggle?.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    themeToggle.innerHTML = isDark ? 
        '<i class="fas fa-sun"></i>' : 
        '<i class="fas fa-moon"></i>';
});

// Navigation Active Link
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    const updateActiveLink = () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', updateActiveLink);

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            navLinks.forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');
        });
    });
}

// Navigation to other pages
function navigateTo(page) {
    window.location.href = page;
}

// Smooth Scroll
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    setupNavigation();
    setupSmoothScroll();
    setupHamburger();
});

// Hamburger Menu
function setupHamburger() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.querySelector('.nav-menu');

    hamburger?.addEventListener('click', () => {
        navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
    });

    // Close menu on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.style.display = 'none';
        });
    });
}

// ============================================
// API Integration Functions
// ============================================

class ResumeAPI {
    static async generateResume(data) {
        try {
            const response = await fetch(`${API_BASE}/resume/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.getToken()}`
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Resume generation failed');
            return await response.json();
        } catch (error) {
            console.error('Error generating resume:', error);
            showNotification('Failed to generate resume', 'error');
            throw error;
        }
    }

    static async exportResume(resumeId, format) {
        try {
            const response = await fetch(
                `${API_BASE}/resume/${resumeId}/export?format=${format}`,
                {
                    headers: {
                        'Authorization': `Bearer ${this.getToken()}`
                    }
                }
            );

            if (!response.ok) throw new Error('Export failed');
            
            // Download file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `resume.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            showNotification('Resume exported successfully!', 'success');
        } catch (error) {
            console.error('Error exporting resume:', error);
            showNotification('Failed to export resume', 'error');
        }
    }

    static getToken() {
        return localStorage.getItem('auth_token') || '';
    }

    static setToken(token) {
        localStorage.setItem('auth_token', token);
    }

    static clearToken() {
        localStorage.removeItem('auth_token');
    }
}

// ============================================
// Notification System
// ============================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <p>${message}</p>
            <button onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 90px;
        right: 20px;
        max-width: 400px;
        border-radius: 8px;
        padding: 1rem;
        z-index: 2000;
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .notification-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: white;
    }

    .notification-content button {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        margin-left: auto;
        font-size: 1.2rem;
    }

    .notification-success {
        background: linear-gradient(135deg, #10b981, #059669);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
    }

    .notification-error {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.3);
    }

    .notification-warning {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.3);
    }

    .notification-info {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
    }

    @media (max-width: 640px) {
        .notification {
            left: 10px;
            right: 10px;
            max-width: none;
        }
    }
`;
document.head.appendChild(notificationStyles);

// ============================================
// Form Utilities
// ============================================

class FormHandler {
    static serializeForm(formElement) {
        const formData = new FormData(formElement);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        
        return data;
    }

    static populateForm(formElement, data) {
        Object.entries(data).forEach(([key, value]) => {
            const field = formElement.elements[key];
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = value;
                } else if (field.type === 'radio') {
                    const radio = formElement.querySelector(`input[name="${key}"][value="${value}"]`);
                    if (radio) radio.checked = true;
                } else {
                    field.value = value;
                }
            }
        });
    }

    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    static validatePhone(phone) {
        const re = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
        return re.test(phone.replace(/\s/g, ''));
    }
}

// ============================================
// Storage Management
// ============================================

class StorageManager {
    static saveResume(resume) {
        const resumes = this.getAllResumes();
        resumes.push({
            ...resume,
            id: Date.now(),
            createdAt: new Date().toISOString()
        });
        localStorage.setItem(`${STORAGE_KEY}_resumes`, JSON.stringify(resumes));
    }

    static getAllResumes() {
        try {
            return JSON.parse(localStorage.getItem(`${STORAGE_KEY}_resumes`)) || [];
        } catch (e) {
            return [];
        }
    }

    static getResume(id) {
        const resumes = this.getAllResumes();
        return resumes.find(r => r.id === id);
    }

    static deleteResume(id) {
        const resumes = this.getAllResumes().filter(r => r.id !== id);
        localStorage.setItem(`${STORAGE_KEY}_resumes`, JSON.stringify(resumes));
    }
}

// ============================================
// Authentication Functions
// ============================================

function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
}

function showSignupModal() {
    document.getElementById('signupModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function switchModal(fromModal, toModal) {
    closeModal(fromModal);
    document.getElementById(toModal).style.display = 'block';
}

// Handle login form submission
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    loginForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        if (email && password) {
            // Simulate login (in real app, this would call an API)
            isAuthenticated = true;
            currentUser = { email };
            localStorage.setItem('cv2desk_user', JSON.stringify(currentUser));
            closeModal('loginModal');
            showNotification('Login successful!', 'success');
            // Redirect to resume builder
            setTimeout(() => {
                window.location.href = 'resume-builder.html';
            }, 1000);
        }
    });

    signupForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        
        if (name && email && password) {
            // Simulate signup (in real app, this would call an API)
            isAuthenticated = true;
            currentUser = { name, email };
            localStorage.setItem('cv2desk_user', JSON.stringify(currentUser));
            closeModal('signupModal');
            showNotification('Account created successfully!', 'success');
            // Redirect to resume builder
            setTimeout(() => {
                window.location.href = 'resume-builder.html';
            }, 1000);
        }
    });

    // Check if user is already logged in
    const savedUser = localStorage.getItem('cv2desk_user');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        isAuthenticated = true;
    }
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// ============================================
// Utility Functions
// ============================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0,
            v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// ============================================
// Page Initialization
// ============================================

// Auto-initialize on page load
window.addEventListener('load', () => {
    console.log('CV2Desk loaded successfully');
});

// Prevent default form submission
document.addEventListener('submit', (e) => {
    if (!e.target.dataset.allowDefault) {
        e.preventDefault();
    }
});
