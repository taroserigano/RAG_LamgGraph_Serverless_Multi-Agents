import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs";
import { getKnowledgeDocuments } from "@/utils/actions";

export async function GET() {
  const { userId } = auth();
  if (!userId) {
    return NextResponse.json({ documents: [] });
  }

  const documents = await getKnowledgeDocuments(userId);
  return NextResponse.json({ documents });
}
