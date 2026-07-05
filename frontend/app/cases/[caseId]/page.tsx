import CaseDetailClient from "@/components/CaseDetailClient";
import { getCase, getCaseComments } from "@/lib/api";
import { Case, CaseComment } from "@/lib/types";

type PageProps = {
  params: Promise<{
    caseId: string;
  }>;
};

export default async function CaseDetailPage({ params }: PageProps) {
  const { caseId } = await params;

  let caseItem: Case | null = null;
  let comments: CaseComment[] = [];

  try {
    caseItem = await getCase(Number(caseId));
    comments = await getCaseComments(Number(caseId));
  } catch {
    caseItem = null;
    comments = [];
  }

  if (!caseItem) {
    return (
      <div>
        <h1 className="mb-4 text-3xl font-bold">Case Not Found</h1>
        <p className="text-slate-400">
          The requested case could not be loaded.
        </p>
      </div>
    );
  }

  return (
    <CaseDetailClient
      caseItem={caseItem}
      initialComments={comments}
    />
  );
}