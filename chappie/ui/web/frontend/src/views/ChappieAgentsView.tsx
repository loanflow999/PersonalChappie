/** Lazy map surface; the parent keeps the existing Agents workspace mounted. */
import { Suspense, lazy } from "react";
import { useLocaleChunk } from "@/i18n";
import type { PlaceId } from "@/components/society/world/islandLayout";

const OfficeStage = lazy(() => import("@/components/society/office/OfficeStage").then((m) => ({ default: m.OfficeStage })));

export interface ChappieAgentsViewProps {
  onSelectAgent?: (agentId: string | null) => void;
  onSelectPlace?: (place: PlaceId) => void;
  onOpenAgents: () => void;
  onCreateAgent?: () => void;
  onOpenGroup?: (groupId: string) => void;
}

export function ChappieAgentsView({ onSelectAgent, onOpenAgents, onCreateAgent, onOpenGroup }: ChappieAgentsViewProps) {
  const ready = useLocaleChunk("society");
  if (!ready) return null;
  return (
    <div className="h-full min-h-0">
      <Suspense fallback={<div className="h-full w-full animate-pulse bg-secondary" aria-hidden />}>
        <OfficeStage onOpenLedger={onOpenAgents} onSelectAgent={onSelectAgent} onCreateAgent={onCreateAgent} onOpenGroup={onOpenGroup} />
      </Suspense>
    </div>
  );
}
