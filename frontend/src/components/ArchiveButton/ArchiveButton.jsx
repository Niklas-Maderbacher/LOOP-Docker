import ConfirmActionModal from '../ConfirmActionModal/ConfirmActionModal.jsx';
import './ArchiveButton.modules.css'
import React, { useState, useEffect } from 'react';

function ArchiveButton({ projectName, actionType }) {
    const [isAdmin, setIsAdmin] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);

    // API-Aufruf, um den Admin-Status zu überprüfen
    useEffect(() => {
        const checkAdminStatus = async () => {
            try {
                const response = await fetch('/users/check/admin', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include', // Wenn Cookies oder Authentifizierung erforderlich sind
                });

                const data = await response.json();

                // Überprüfen, ob der Benutzer ein Admin ist
                setIsAdmin(data.admin_state || false);
            } catch (error) {
                console.error('Error fetching admin status:', error);
                setIsAdmin(false);
            } finally {
                setIsLoading(false);
            }
        };

        checkAdminStatus();
    }, []);

    // Funktion zum Öffnen des Modals
    const handleClick = () => {
        setIsModalOpen(true);
    };

    // Bestätigung (Ja) vom Benutzer
    const handleConfirm = (actionType) => {
        if (actionType === 'archive') {
            archiveProject();
        } else if (actionType === 'unarchive') {
            unarchiveProject();
        }
        setIsModalOpen(false);
    };

    // Abbruch (Nein) durch den Benutzer
    const handleCancel = () => {
        alert("Action cancelled!");
        setIsModalOpen(false);
    };

    // Beispiel für API-Aufrufe (Archivieren/Wiederherstellen)
    const archiveProject = () => {
        alert(`Project "${projectName}" has been archived!`);
        // Ersetze dies mit dem tatsächlichen API-Aufruf
        // fetch('/api/archive', { method: 'POST', body: JSON.stringify({ projectName }) });
    };

    const unarchiveProject = () => {
        alert(`Project "${projectName}" has been unarchived!`);
        // Ersetze dies mit dem tatsächlichen API-Aufruf
        // fetch('/api/unarchive', { method: 'POST', body: JSON.stringify({ projectName }) });
    };

    // Wenn die Daten noch geladen werden, zeige den Ladeindikator
    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            {/* Button nur anzeigen, wenn der Benutzer Admin ist */}
            {isAdmin && (
                <button className="archive-button" onClick={handleClick}>
                    <img className="archive-unarchive-image" src="/icons/archive.svg" alt="Icon" width="24" height="24"/>
                </button>
            )}

            {/* Modal anzeigen, wenn es geöffnet ist */}
            {isModalOpen && (
                <ConfirmActionModal
                    message={`Do you want to ${actionType} the following project: ${projectName}`}
                    actionType={actionType}
                    onConfirm={handleConfirm}
                    onCancel={handleCancel}
                />
            )}
        </div>
    );
}

export default ArchiveButton;
