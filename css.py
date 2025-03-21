CUSTOM_CSS = """
<style>
    .stApp { 
        background: linear-gradient(135deg, #000000 0%, #2a5298 100%);
        color: white;
    }
    .stButton>button { 
        background: #63c5da !important;
        color: white !important;
        transition: all 0.3s ease !important;
        border: none;
    }
    .stButton>button:hover { 
        background: #000000 !important;
        transform: scale(1.05);
    }
    .diagnosis-card {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        margin: 1rem 0;
    }
    .footer { 
        color: rgba(255, 255, 255, 0.6) !important;
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
    }
    .image-column { 
        padding-right: 3rem;
    }
    @keyframes slideIn {
        0% { transform: translateY(-20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes pulse-positive {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.4); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(0, 255, 136, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }
    @keyframes pulse-warning {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 118, 117, 0.7); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(255, 118, 117, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 118, 117, 0); }
    }
    @keyframes pulse-alert {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(255, 71, 87, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 71, 87, 0); }
    }
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .pulse-positive {
        animation: pulse-positive 1.5s ease-out infinite;
    }
    .pulse-warning {
        animation: pulse-warning 1.5s ease-out infinite;
    }
    .pulse-alert {
        animation: pulse-alert 1.5s ease-out infinite;
    }
    .floating-emoji {
        animation: floating 2s ease-in-out infinite;
        display: inline-block;
    }
    .doctor-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
"""