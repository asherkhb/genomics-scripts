# Source: http://bioconductor.org/packages/release/bioc/vignettes/GENESIS/inst/doc/pcair.R
# Help: http://bioconductor.org/packages/release/bioc/vignettes/GENESIS/inst/doc/pcair.html

library(GENESIS)
library(GWASTools)
library(SNPRelate)

#inPlink <- "RA/assoc/ra.allCommon.placebo.filtered"
#inPlink <- "SLE/assoc/sle.allCommon.placebo.filtered"
#inPlink <- "asthma/assoc/asthma.allCommon.placebo.eur.1.filtered"
#inPlink <- "AMD/assoc/amd.allCommon.allSamples.filtered"
#inPlink <- "alzheimers/assoc/alz.placebo.filtered.eur"
#inPlink <- "SLE2/assoc/sle.placebo.eur.filtered"
#inPlink <- "alzheimers2/assoc/alz.old.placebo.eur.filtered"
#inPlink <- "asthma2/assoc/asthma.placebo.eur.filtered"
#inPlink <- "RA2/assoc/ra.placebo.eur.filtered"
#inPlink <- "merge/ra_asthma_alz_sle.placebo.eur.filtered.no-missnp"
#inPlink <- "DR/assoc/dr.placebo.eur.filtered"
inPlink <- "COPD/assoc/copd.placebo.eur.filtered"

#load("asthma/assoc/asthma.allCommon.placebo.eur.1.filtered.mypcair.RData")
#load("asthma/assoc/asthma.allCommon.placebo.eur.1.filtered.mypcrelate.RData")
#load("asthma/assoc/asthma.allCommon.placebo.eur.1.filtered.kinship.RData")
#load("asthma/assoc/asthma.allCommon.placebo.eur.1.filtered.inbreed.RData")

## Prepare Data ##
# Create .gds from PLINK data.
snpgdsBED2GDS(bed.fn = paste0(inPlink, ".bed"),
              fam.fn = paste0(inPlink, ".fam"),
              bim.fn = paste0(inPlink, ".bim"),
              out.gdsfn = paste0(inPlink, ".gds"))

# Generate KING data.
gf <- snpgdsOpen(paste0(inPlink, ".gds")) # openfn.gds(paste0(inPlink, ".gds"))
gf <- snpgdsOpen("asthma_QCd/asthma.placebo.eur.filtered.hwe10e-3.gds")
ibd.king <- snpgdsIBDKING(gf, num.thread=20)
KINGmat <- ibd.king$kinship
rownames(KINGmat) <- ibd.king$sample.id
colnames(KINGmat) <- ibd.king$sample.id
snpgdsClose(gf) # closefn.gds(gf)
KINGmat[1:10,1:10]

# Read in GDS data & create GenotypeData object.
genoData <- GenotypeData(GdsGenotypeReader(filename = paste0(inPlink, ".gds")))
genoData

## Principal Components Analysis in Related Samples (PC-AiR) ##

# Pairwise Measures of Ancestry Divergence.
# ... Read individual IDs from GenotypeData object.
iids <- getScanID(genoData)
head(iids)

# ... Run PC-AiR.
## RELATED OPTION
mypcair <- pcair(genoData = genoData, kinMat = KINGmat, divMat = KINGmat)
## UNRELATED OPTION
mypcair <- pcair(genoData = genoData, divMat = KINGmat)

save(mypcair, file = paste0(inPlink, ".pcair.RData"))
png(paste0(inPlink, ".pcair.png"), width=500, height=500)
plot(mypcair)
dev.off()
write.table(mypcair$vectors, paste0(inPlink, ".evs.tsv"), sep="\t", row.names=TRUE, quote=FALSE)

# ... Check results.
summary(mypcair)
plot(mypcair)

png(paste0(inPlink, ".pcair.png"), width=500, height=500)
plot(mypcair)
dev.off()

# ... Write EVs to file.
write.table(mypcair$vectors, paste0(inPlink, ".evs.tsv"), sep="\t", row.names=TRUE, quote=FALSE)

# Kinship & Inbreeding: PC-Relate

# ... Run PC-AiR Partition.
part <- pcairPartition(kinMat = KINGmat, divMat = KINGmat)

head(part$unrels)
head(part$rels)

# ... Run PC-Relace.
mypcrelate <- pcrelate(genoData = genoData, pcMat = mypcair$vectors[,1:2],
                       training.set = mypcair$unrels)

# ... Check Kinship.
kinship <- pcrelateReadKinship(pcrelObj = mypcrelate, scan.include = iids)
hist(kinship$kin)
plot(kinship$k0, kinship$k1)

sampExclude <- as.character(unlist(subset(kinship, kin > 0.1, select="ID1")))
sampExclude <- unique(c(sampExclude, as.character(unlist(subset(kinship, k0 < 0.6, select="ID1")))))
write.table(sampExclude, paste0(inPlink, ".excludeSamples.lst"), quote=FALSE, row.names=FALSE, col.names = FALSE)

# ... Evaluate Inbreeding
inbreed <- pcrelateReadInbreed(pcrelObj = mypcrelate, scan.include = iids)
hist(inbreed$f)

# Close genoData object.
close(genoData)


plink1.9 --bfile ra.allCommon.placebo.filtered --logistic hide-covar --ci 0.95 --pheno placebo_rsp.lst --pheno-name RESPONSE --covar placebo_cof.lst --covar-name AGE,SEX,BASELINE,EV1,EV2,EV3,EV4,EV5 --out ra.allCommon.placebo.res03
