import KnowledgeVault from "@/components/KnowledgeVault";
import { auth } from "@clerk/nextjs";
import { redirect } from "next/navigation";
import { getKnowledgeDocuments } from "@/utils/actions";

const VaultPage = async () => {
  const { userId } = auth();
  if (!userId) {
    redirect("/sign-in");
  }

  const documents = await getKnowledgeDocuments(userId);
  return <KnowledgeVault userId={userId} initialDocuments={documents} />;
};

export default VaultPage;
