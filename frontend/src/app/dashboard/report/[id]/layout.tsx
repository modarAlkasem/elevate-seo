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
    title: `ElevateSEO - Report Status (Snapshot ID: ${id})`,
  };
};

const ReportStatusLayout = ({ children }: { children: React.ReactNode }) => {
  return <> {children}</>;
};

export default ReportStatusLayout;
