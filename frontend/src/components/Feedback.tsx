import { userMessageFor } from '../lib/apiErrors';

export function LoadingMessage({ text }: { text: string }) {
  return (
    <p className="feedback" aria-live="polite">
      {text}
    </p>
  );
}

export function AlertMessage({ text }: { text: string }) {
  return (
    <p className="feedback feedback-error" role="alert">
      {text}
    </p>
  );
}

export function ErrorMessage({ error }: { error: Error }) {
  return <AlertMessage text={userMessageFor(error)} />;
}
