import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Shield } from 'lucide-react';

const AdminKYC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">KYC Verification</h1>
        <p className="text-slate-600 mt-1">Verify user identity documents</p>
      </div>

      <Card>
        <CardContent className="p-12">
          <div className="text-center">
            <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <Shield className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">KYC Verification System</h3>
            <p className="text-slate-600">Full KYC verification interface will be available here</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminKYC;