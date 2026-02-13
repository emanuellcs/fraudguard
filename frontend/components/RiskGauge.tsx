import { cn } from "@/lib/utils";

export function RiskGauge({ score }: { score: number }) {
  const percentage = Math.round(score * 100);
  const isHighRisk = score > 0.5;

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-slate-900 rounded-xl border border-slate-800">
      <h3 className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-4">Fraud Probability</h3>
      
      <div className="relative w-48 h-24 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-slate-800 rounded-t-full"></div>
        <div 
          className={cn(
            "absolute top-0 left-0 w-full h-full rounded-t-full transition-all duration-700 ease-out origin-bottom",
            isHighRisk ? "bg-red-500" : "bg-emerald-500"
          )}
          style={{ transform: `rotate(${(percentage / 100) * 180 - 180}deg)` }}
        ></div>
      </div>
      
      <div className="mt-2 text-4xl font-bold text-white">
        {percentage}%
      </div>
      <div className={cn(
        "mt-1 px-3 py-1 rounded-full text-xs font-bold uppercase",
        isHighRisk ? "bg-red-500/20 text-red-400" : "bg-emerald-500/20 text-emerald-400"
      )}>
        {isHighRisk ? "CRITICAL RISK" : "SAFE"}
      </div>
    </div>
  );
}