#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  stop("Exactly 1 input PLINK file must be specified.", call.=FALSE)
} else {
  library(GENESIS)
  library(GWASTools)
  library(SNPRelate)

  inPlink = args[1]

  # Create .gds from PLINK data.
  print("Creating GDS File...")
  snpgdsBED2GDS(bed.fn = paste0(inPlink, ".bed"),
                fam.fn = paste0(inPlink, ".fam"),
                bim.fn = paste0(inPlink, ".bim"),
                out.gdsfn = paste0(inPlink, ".gds"))

  # Run KING
  print("Running KING...")
  gf <- snpgdsOpen(paste0(inPlink, ".gds"))
  ibd.king <- snpgdsIBDKING(gf, num.thread=10)
  KINGmat <- ibd.king$kinship
  rownames(KINGmat) <- ibd.king$sample.id
  colnames(KINGmat) <- ibd.king$sample.id
  snpgdsClose(gf)

  # Read GENO data.
  print("Building Genotype Data...")
  genoData <- GenotypeData(GdsGenotypeReader(filename = paste0(inPlink, ".gds")))
  iids <- getScanID(genoData)

  # Run PC-AiR
  print("Running PC-AiR...")

  # mypcair <- pcair(genoData = genoData, kinMat = KINGmat, divMat = KINGmat)
  mypcair <- pcair(genoData = genoData, divMat = KINGmat)
  save(mypcair, file = paste0(inPlink, ".pcair.RData"))

  # Write EVs to file.
  print("Writing results...")
  # ... EV table
  write.table(mypcair$vectors, paste0(inPlink, ".evs.tsv"), sep="\t", row.names=TRUE, quote=FALSE)
  # ... PCAir Plot.
  png(paste0(inPlink, ".pcair.png"), width=950, height=500)
  plot(mypcair)
  dev.off()

  print(paste0("Complete! See ", inPlink, "{.evs.tsv, .pcair.png, .pcair.RData, .gds}"))
}
