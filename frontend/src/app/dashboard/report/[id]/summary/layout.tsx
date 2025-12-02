import type { Metadata, ResolvingMetadata } from "next";

type Props = {
  params: Promise<{ id: string }>;
};

export const generateMetadata = async (
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> => {
  const { id } = await params;
  return {
    title: `ElevateSEO - Report Summary (Snapshot ID: ${id})`,
  };
};

const ReportSummary = ({ children }: { children: React.ReactNode }) => {
  return <> {children}</>;
};

export default ReportSummary;
