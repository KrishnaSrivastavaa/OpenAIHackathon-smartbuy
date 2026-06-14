import { HTMLAttributes } from 'react';
import { cn } from '../../lib/utils';
export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) { return <div className={cn('rounded-3xl border border-slate-200 bg-white p-5 shadow-xl shadow-slate-200/60', className)} {...props} />; }
