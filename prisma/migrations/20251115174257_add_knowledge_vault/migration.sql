-- CreateEnum
CREATE TYPE "KnowledgeStatus" AS ENUM ('PROCESSING', 'PROCESSED', 'FAILED');

-- CreateTable
CREATE TABLE "KnowledgeDocument" (
    "id" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "userId" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "mimeType" TEXT NOT NULL,
    "size" INTEGER NOT NULL,
    "chunkCount" INTEGER NOT NULL DEFAULT 0,
    "tokenEstimate" INTEGER NOT NULL DEFAULT 0,
    "status" "KnowledgeStatus" NOT NULL DEFAULT 'PROCESSING',
    "error" TEXT,
    "notes" TEXT,
    "sourceUrl" TEXT,

    CONSTRAINT "KnowledgeDocument_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "KnowledgeDocument_userId_idx" ON "KnowledgeDocument"("userId");
