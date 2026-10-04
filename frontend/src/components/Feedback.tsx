import { userMessageFor } from '../lib/apiErrors';

export function LoadingMessage({ text }: { text: string }) {
  return (
    <p className="feedback" aria-live="polite">
      {text}
    </p>
  );
}

export function ErrorMessage({ error }: { error: Error }) {
  return (
    <p className="feedback feedback-error" role="alert">
      {userMessageFor(error)}
    </p>
  );
}
