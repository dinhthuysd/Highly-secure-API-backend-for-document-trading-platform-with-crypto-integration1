import api from './api';

class AdminService {
  // ============ AUTHENTICATION ============
  
  async login(email, password, totpCode = null) {
    const response = await api.post('/admin/auth/login', {
      email,
      password,
      totp_code: totpCode,
    });
    
    if (response.data.access_token) {
      localStorage.setItem('admin_token', response.data.access_token);
    }
    
    return response.data;
  }
  
  async getProfile() {
    const response = await api.get('/admin/auth/profile');
    localStorage.setItem('admin_user', JSON.stringify(response.data));
    return response.data;
  }
  
  async updateProfile(data) {
    const response = await api.put('/admin/auth/profile', data);
    return response.data;
  }
  
  async changePassword(oldPassword, newPassword) {
    const response = await api.post('/admin/auth/change-password', {
      old_password: oldPassword,
      new_password: newPassword,
    });
    return response.data;
  }
  
  async logout() {
    try {
      await api.post('/admin/auth/logout');
    } finally {
      localStorage.removeItem('admin_token');
      localStorage.removeItem('admin_user');
    }
  }
  
  // ============ DASHBOARD ============
  
  async getDashboardStats() {
    const response = await api.get('/admin/dashboard');
    return response.data;
  }
  
  // ============ USER MANAGEMENT ============
  
  async getUsers(params = {}) {
    const response = await api.get('/admin/users', { params });
    return response.data;
  }
  
  async getUserDetail(userId) {
    const response = await api.get(`/admin/users/${userId}`);
    return response.data;
  }
  
  async updateUserStatus(userId, isActive) {
    const response = await api.put(`/admin/users/${userId}/status`, null, {
      params: { is_active: isActive },
    });
    return response.data;
  }
  
  // ============ KYC MANAGEMENT ============
  
  async getPendingKYC(params = {}) {
    const response = await api.get('/admin/kyc/pending', { params });
    return response.data;
  }
  
  async verifyKYC(kycId, approved, adminNote = null) {
    const response = await api.put(`/admin/kyc/${kycId}/verify`, null, {
      params: { approved, admin_note: adminNote },
    });
    return response.data;
  }
  
  // ============ DOCUMENT MANAGEMENT ============
  
  async getDocuments(params = {}) {
    const response = await api.get('/admin/documents', { params });
    return response.data;
  }
  
  async approveDocument(docId, approved, adminNote = null) {
    const response = await api.put(`/admin/documents/${docId}/approve`, null, {
      params: { approved, admin_note: adminNote },
    });
    return response.data;
  }
  
  // ============ DEPOSIT MANAGEMENT ============
  
  async getDeposits(params = {}) {
    const response = await api.get('/admin/deposits', { params });
    return response.data;
  }
  
  async processDeposit(depositId, approved, adminNote = null) {
    const response = await api.put(`/admin/deposits/${depositId}/process`, null, {
      params: { approved, admin_note: adminNote },
    });
    return response.data;
  }
  
  // ============ WITHDRAWAL MANAGEMENT ============
  
  async getWithdrawals(params = {}) {
    const response = await api.get('/admin/withdrawals', { params });
    return response.data;
  }
  
  async processWithdrawal(withdrawalId, approved, adminNote = null) {
    const response = await api.put(`/admin/withdrawals/${withdrawalId}/process`, null, {
      params: { approved, admin_note: adminNote },
    });
    return response.data;
  }
  
  // ============ TRANSACTIONS ============
  
  async getTransactions(params = {}) {
    const response = await api.get('/admin/transactions', { params });
    return response.data;
  }
  
  // ============ AUDIT LOGS ============
  
  async getAuditLogs(params = {}) {
    const response = await api.get('/admin/audit-logs', { params });
    return response.data;
  }
}

export default new AdminService();