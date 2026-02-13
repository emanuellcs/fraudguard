import { TransactionResponse } from "@/lib/api";
import { ShieldAlert, ShieldCheck } from "lucide-react";

export function HistoryTable({ transactions }: { transactions: TransactionResponse[] }) {
  return (
    <div className="w-full overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50">
      <table className="w-full text-left text-sm text-slate-400">
        <thead className="bg-slate-900 text-slate-200 uppercase font-medium">
          <tr>
            <th className="px-6 py-4">Transaction ID</th>
            <th className="px-6 py-4">Risk Score</th>
            <th className="px-6 py-4">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {transactions.map((txn) => (
            <tr key={txn.transaction_id} className="hover:bg-slate-800/50 transition-colors">
              <td className="px-6 py-4 font-mono text-xs text-slate-500">
                {txn.transaction_id.slice(0, 8)}...
              </td>
              <td className="px-6 py-4">
                {(txn.risk_score * 100).toFixed(1)}%
              </td>
              <td className="px-6 py-4">
                <div className="flex items-center gap-2">
                  {txn.is_fraud ? (
                    <>
                      <ShieldAlert className="w-4 h-4 text-red-500" />
                      <span className="text-red-400 font-medium">Suspicious</span>
                    </>
                  ) : (
                    <>
                      <ShieldCheck className="w-4 h-4 text-emerald-500" />
                      <span className="text-emerald-400 font-medium">Safe</span>
                    </>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}