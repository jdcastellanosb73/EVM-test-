import { useEffect, useId, useRef, type ReactNode } from 'react';

interface ModalProps {
  title: string;
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

/** Native <dialog>: focus trap, Escape to close and backdrop come from the browser. */
export function Modal({ title, open, onClose, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const titleId = useId();

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) {
      return;
    }
    if (open && !dialog.open) {
      dialog.showModal();
    } else if (!open && dialog.open) {
      dialog.close();
    }
  }, [open]);

  return (
    <dialog ref={dialogRef} className="modal" aria-labelledby={titleId} onClose={onClose}>
      <header className="modal-header">
        <h2 id={titleId}>{title}</h2>
        <button type="button" className="button-icon" aria-label="Cerrar" onClick={onClose}>
          ×
        </button>
      </header>
      {open && children}
    </dialog>
  );
}
