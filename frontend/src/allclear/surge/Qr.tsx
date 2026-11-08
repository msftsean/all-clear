import { useEffect, useState } from "react";
import QRCode from "qrcode";

// Renders a QR code for `value` as an <img>. Generated locally (no external
// QR service), so it works on venue Wi-Fi with no extra network dependency.
export default function Qr({
  value,
  size = 240,
  dark = "#070b1a",
  light = "#ffffff",
  label,
}: {
  value: string;
  size?: number;
  dark?: string;
  light?: string;
  label?: string;
}) {
  const [src, setSrc] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    QRCode.toDataURL(value, {
      width: size * 2,
      margin: 1,
      errorCorrectionLevel: "M",
      color: { dark, light },
    })
      .then((url) => alive && setSrc(url))
      .catch(() => alive && setSrc(null));
    return () => {
      alive = false;
    };
  }, [value, size, dark, light]);

  return (
    <div
      data-testid="surge-qr"
      style={{ width: size, height: size }}
      className="overflow-hidden rounded-bubble bg-white"
    >
      {src ? (
        <img src={src} width={size} height={size} alt={label || `QR code for ${value}`} />
      ) : (
        <div className="flex h-full items-center justify-center p-3 text-center font-mono text-xs text-inkwarm">
          {value}
        </div>
      )}
    </div>
  );
}
