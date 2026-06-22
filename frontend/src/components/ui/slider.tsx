import * as React from "react";
import { cn } from "@/lib/utils";

interface SliderProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  valueLabel?: string;
}

const Slider = React.forwardRef<HTMLInputElement, SliderProps>(
  ({ className, label, valueLabel, ...props }, ref) => {
    return (
      <div className={cn("space-y-3", className)}>
        {label ? (
          <div className="flex items-center justify-between text-sm text-slate-300">
            <label>{label}</label>
            {valueLabel ? <span className="text-slate-500">{valueLabel}</span> : null}
          </div>
        ) : null}
        <input
          ref={ref}
          type="range"
          className="h-2 w-full cursor-pointer appearance-none rounded-full bg-slate-800 accent-sky-400 outline-none transition hover:brightness-110"
          {...props}
        />
      </div>
    );
  }
);
Slider.displayName = "Slider";

export { Slider };
