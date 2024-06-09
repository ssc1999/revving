// src/components/InvoiceApp.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logo from '../assets/logo.webp'; // Adjust the path as necessary

const InvoiceApp = () => {
    const [totals, setTotals] = useState([]);
    const [invoices, setInvoices] = useState([]);
    const [page, setPage] = useState(1);
    const [totalsAvailable, setTotalsAvailable] = useState(false);
    const [invoicesAvailable, setInvoicesAvailable] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [view, setView] = useState('totals'); // 'totals' or 'invoices'
    const [message, setMessage] = useState(null);

    useEffect(() => {
        if (view === 'totals') {
            loadTotals();
        } else {
            loadInvoices(page);
        }
    }, [view, page]);

    const loadTotals = async () => {
        try {
            const response = await axios.get('/api/invoice-totals/');
            if (response.data.status === 'fail') {
                setTotalsAvailable(false);
            } else {
                setTotals(response.data);
                setTotalsAvailable(true);
            }
        } catch (error) {
            console.error('Error loading totals:', error);
            setTotalsAvailable(false);
        }
    };

    const loadInvoices = async (page) => {
        try {
            const response = await axios.get(`/api/invoices/?page=${page}`);
            if (response.data.invoices && response.data.invoices.length > 0) {
                setInvoices(response.data.invoices);
                setInvoicesAvailable(true);
            } else {
                setInvoices([]);
                setInvoicesAvailable(false);
            }
        } catch (error) {
            console.error('Error loading invoices:', error);
            setInvoicesAvailable(false);
        }
    };

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            setMessage({ type: 'error', text: 'Please select a file to upload.' });
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const uploadResponse = await axios.post('/api/upload-invoice/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (uploadResponse.data.status === 'success') {
                setMessage({ type: 'success', text: 'File uploaded successfully.' });
            } else {
                setMessage({ type: 'error', text: 'File upload failed.' });
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage({ type: 'error', text: 'Error uploading file.' });
        }
    };

    const handleRefresh = () => {
        if (view === 'totals') {
            loadTotals();
        } else {
            loadInvoices(1); // Reset to the first page on refresh
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-periwinkle">
            <div className="container mx-auto p-4">
                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-4xl font-bold text-medium_slate_blue">Tech Task</h1>
                    <img src={logo} alt="Logo" className="w-24 h-24" />
                </div>
                <h2 className="text-2xl font-bold text-medium_slate_blue mb-4">Upload Invoices</h2>
                <div className="mb-4">
                    <input type="file" onChange={handleFileChange} className="p-2 border rounded bg-dim_gray text-midnight_blue" />
                    <button onClick={handleFileUpload} className="ml-4 p-2 bg-medium_slate_blue text-white rounded">Upload File</button>
                </div>
                {message && (
                    <div className={`mb-4 p-2 rounded ${message.type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white`}>
                        {message.text}
                    </div>
                )}
                <button
                    onClick={() => setView(view === 'totals' ? 'invoices' : 'totals')}
                    className="mb-4 p-2 bg-medium_slate_blue text-white rounded animate-scale"
                >
                    {view === 'totals' ? 'View All Invoices' : 'View Invoice Totals'}
                </button>
                {view === 'totals' && totalsAvailable && (
                    <div className="mb-8">
                        <h2 className="text-xl font-semibold text-medium_slate_blue mb-2">Invoice Totals</h2>
                        <table className="min-w-full bg-english_violet border text-periwinkle">
                            <thead>
                                <tr className="bg-medium_slate_blue text-white">
                                    <th className="py-2">Revenue Source</th>
                                    <th className="py-2">Total Value</th>
                                    <th className="py-2">Total Advance</th>
                                    <th className="py-2">Total Expected Fee</th>
                                </tr>
                            </thead>
                            <tbody>
                                {totals.map((total, index) => (
                                    <tr key={index} className="border-t border-periwinkle">
                                        <td className="py-2 px-4">{total.revenue_source}</td>
                                        <td className="py-2 px-4">{total.total_value}</td>
                                        <td className="py-2 px-4">{total.total_advance}</td>
                                        <td className="py-2 px-4">{total.total_expected_fee}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
                {view === 'invoices' && invoicesAvailable && (
                    <div>
                        <h2 className="text-xl font-semibold text-medium_slate_blue mb-2">All Invoices</h2>
                        <table className="min-w-full bg-english_violet border text-periwinkle">
                            <thead>
                                <tr className="bg-medium_slate_blue text-white">
                                    <th className="py-2">Invoice Number</th>
                                    <th className="py-2">Customer</th>
                                    <th className="py-2">Date</th>
                                    <th className="py-2">Value</th>
                                    <th className="py-2">Haircut Percentage</th>
                                    <th className="py-2">Daily Fee</th>
                                    <th className="py-2">Currency</th>
                                    <th className="py-2">Revenue Source</th>
                                    <th className="py-2">Expected Duration</th>
                                </tr>
                            </thead>
                            <tbody>
                                {invoices.map((invoice, index) => (
                                    <tr key={index} className="border-t border-periwinkle">
                                        <td className="py-2 px-4">{invoice.invoice_number}</td>
                                        <td className="py-2 px-4">{invoice.customer}</td>
                                        <td className="py-2 px-4">{invoice.date}</td>
                                        <td className="py-2 px-4">{invoice.value}</td>
                                        <td className="py-2 px-4">{invoice.haircut_percentage}</td>
                                        <td className="py-2 px-4">{invoice.daily_fee}</td>
                                        <td className="py-2 px-4">{invoice.currency}</td>
                                        <td className="py-2 px-4">{invoice.revenue_source}</td>
                                        <td className="py-2 px-4">{invoice.expected_duration}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <div className="mt-4 flex justify-between">
                            <button onClick={() => setPage(page - 1)} disabled={page === 1} className="p-2 bg-dim_gray text-white rounded disabled:opacity-50">Previous</button>
                            <button onClick={() => setPage(page + 1)} className="p-2 bg-dim_gray text-white rounded">Next</button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default InvoiceApp;
