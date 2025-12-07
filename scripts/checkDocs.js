const { PrismaClient } = require("@prisma/client");

async function main() {
  const prisma = new PrismaClient();
  try {
    const docs = await prisma.knowledgeDocument.findMany({
      orderBy: { createdAt: "desc" },
      take: 5,
    });
    console.log(JSON.stringify(docs, null, 2));
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
