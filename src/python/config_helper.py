import pandas as pd
import os

class ConfigHelper:
    
    def __init__(self, config):
        self.config = config
        
        # sample-file mappping: reading and cleaning 
        #  SAMPLE_FILE_MAPPING has to have the following structure:
        #  [ID | FILE | ASSAY ] , ASSAY can be for example RNA_Seq
        df_mapping = pd.read_csv(self.config["wb"], sep='\t')
        if not list(df_mapping.columns.values)==["ID", "FILE", "ASSAY"]:
            print("File does not correspond to required format with columns [ID | FILE | ASSAY]")
        df_mapping = df_mapping.dropna()
        # Check if file exists 
        df_mapping["existent"] = [os.path.exists(x) for x in df_mapping["FILE"]]
        df_mapping = df_mapping[df_mapping["existent"]]
        self.sample_file_mapping = df_mapping
        
        # sample annotation
        #  SAMPLE_ANNOTATION must have assay names as specified in sample-file mappping for ID columns
        sa_file = self.config["SAMPLE_ANNOTATION"]
        self.sample_annotation = pd.read_csv(sa_file, sep='\t')
        print(self.sample_annotation.head(5))
        
        # OUTRIDER ids
        self.outrider_all, self.outrider_filtered = self.createOutriderIds(min_ids=config["min_outrider_ids"])
    
    """ 
    Get directory path for processed results
    """
    def getProcResultsDir(self):
        return self.config["PROC_RESULTS"] + "/" + self.config["PROJECT_NAME"]
    
    """ 
    Get directory path for processed data
    """
    def getProcDataDir(self):
        return self.config["PROC_DATA"] + "/" + self.config["PROJECT_NAME"]
    
    """
    Get sample ID by experiment
    """
    def getSampleIDs(self, experiment):
        # deprecated for all_vcf
        return list(self.sample_file_mapping[self.sample_file_mapping["ASSAY"] == experiment][["ID"]]) 
        
    """
    Create a full and filtered list of RNA assay IDs subsetted by specified OUTRIDER groups
    """
    def createOutriderIds(self, min_ids=40):
        # deprecated for outrider_files
        
        outrider_group = self.config["outrider_group"]
        rna_assay = self.config["rna_assay"]
        ids = self.getSampleIDs(self.config["rna_assay"])
        
        # Get unique outrider Groups
        df_outrider = self.sample_annotation[self.sample_annotation[rna_assay].isin(ids)]
        df_outrider = df_outrider[[rna_assay, outrider_group]].drop_duplicates().copy()
        
        # assumes that OUTRIDER groups are comma-separated
        # get unique group names
        outrider_groups = []
        for s in set(df_outrider[[outrider_groups]]):
            outrider_groups.extend(s.split(',').strip())
            
        # collect IDs per group
        outrider_ids = {og : df_outrider.loc[df_outrider[outrider_group].str.contains('(^|,)' + og + '(,|$)'), rna_assay].tolist() for og in set(outrider_groups)}
        
        return outrider_ids, {og: _list for og, _list in outrider_ids.items() if len(_list) > min_ids}
    
    """
    Get lists of IDs per OUTRIDER group as (all ids, filtered ids)
    """
    def getOutriderIds(self):
        return self.outrider_all, self.outrider_filtered
    
    """
    Wrapper for getting count file for OUTRIDER group
    """
    def getCountFileByOutriderGroup(self, group):
        return expand(self.getProcResultsDir() + "/{{annotation}}/counts/{sampleID}.Rds", sampleID=self.outrider_all[group])
    
    """
    TODO: do this
    """
    def getMaeFiles(self):
        # rna and exome are the names of the experiments specified in the mapping file
        
        rna_assay = self.config["rna_assay"]
        dna_assay = self.config["dna_assay"]
        
        # return nothing, if there aren't any exomes
        if dna_assay not in self.sample_annotation.columns:
            return []
        
        rna = self.getSampleIDs(rna_assay)
        vcf = self.getSampleIDs(dna_assay)
        
        ### TODO: Check if both RNA and DNA for a file exist at the same time
        return vcf, rna   

        
        
#    def mae_files(sa_file = config["SAMPLE_ANNOTATION"]):
#        
#        anno = pd.read_csv(sa_file, sep='\t')
#        
#        # subset and clean
#        anno_mae = anno[anno["LAB"] == "PROKISCH"]
#        anno_mae = anno_mae[pd.notnull(anno_mae.EXOME_ID)]
#        anno_mae = anno_mae[pd.notnull(anno_mae.RNA_ID)]
#        anno_mae = anno_mae[["EXOME_ID", "RNA_ID"]].copy()
#    
#        # create file names
#        # anno_mae['rna_file'] = [config["RAW_DATA"] + "/" + x + "/RNAout/paired-endout/stdFilenames/" + x + ".bam" for x in anno_mae["RNA_ID"]]
#        # anno_mae['vcf_file'] = [config["RAW_DATA"] + "/" + x + "/exomicout/paired-endout/stdFilenames/" + x + ".vcf.gz" for x in anno_mae["EXOME_ID"]]
#        
#       anno_mae['rna_file'] = [config["RAW_DATA"] + "/" + x + "/RNAout" for x in anno_mae["RNA_ID"]]
#       anno_mae['vcf_file'] = [config["RAW_DATA"] + "/" + x + "/exomicout" for x in anno_mae["EXOME_ID"]]
#    
#        # check for missing files
#        anno_mae['vcf_exists'] = [os.path.exists(x) for x in anno_mae["vcf_file"]]
#        anno_mae['rna_exists'] = [os.path.exists(x) for x in anno_mae["rna_file"]]
#        anno_mae = anno_mae[anno_mae['vcf_exists'] & anno_mae['rna_exists']]
#        
#        vcf = anno_mae["EXOME_ID"] 
#        rna = anno_mae["RNA_ID"]
#        
#        return vcf.tolist(), rna.tolist()

        