import './ConfirmActionModal.modules.css'
import React, { useState } from 'react';

function ConfirmActionModal({ message, actionType, onConfirm, onCancel }) {
    return (
        <div className="modal">
            <div className="modal-content">
                <h2>{message}</h2>
                <button onClick={() => onConfirm(actionType)}>Yes</button>
                <button onClick={onCancel}>No</button>
            </div>
        </div>
    );
}

export default ConfirmActionModal;
