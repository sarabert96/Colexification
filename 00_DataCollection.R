#This script writes a CSV with the data from CLICS3, enriched with Concepticon's MRC data

#See https://github.com/clics/clics3 for details on how to create the sqlite CLICS database
#The remainder of the code is an adaptation of the CLICS2 cookbook https://github.com/clics/clics2/tree/master/cookbook, and an enrichment using CONCEPTICON's MRC data
#Concepticon:https://concepticon.clld.org/
#MRC: http://websites.psychology.uwa.edu.au/school/MRCDataBase/uwa_mrc.htm

if (!file.exists('../data/clics/df_all_raw.csv')){
    library("dplyr")
    library("readr")
    library(DBI)

    concepticon_path = '../data/local/concepticon-data/'
    clics_path= '../data/local/clics3/'
    path_to_db <- paste(clics_path,'clics.sqlite', sep='')
    db <- dbConnect(RSQLite::SQLite(), path_to_db)
    df <- dbGetQuery(db, 'SELECT
        f.dataset_ID, f.ID as Form_ID, f.Form, f.clics_form,
        p.name as gloss_in_source, p.Concepticon_ID, p.Concepticon_Gloss,p.Ontological_Category,p.Semantic_Field,
        l.Name as variety, l.Glottocode, l.ISO639P3code, l.Macroarea, l.Family, l.Latitude, l.Longitude
    FROM
        formtable as f, parametertable as p, languagetable as l
    WHERE
        f.dataset_ID = p.dataset_ID AND f.parameter_ID = p.ID
        AND f.dataset_ID = l.dataset_ID AND f.language_ID = l.ID
    ORDER BY
        f.dataset_ID, p.ID, l.ID;')

    #Joining MRC data
    mrc <- read_tsv(paste(concepticon_path,'concepticondata/concept_set_meta/mrc.tsv',sep=''))
    mrc$CONCEPTICON_ID <- as.character(mrc$CONCEPTICON_ID) #coerce type to join on CLICS3
    df <- left_join(df,mrc,
                     by=c("Concepticon_ID" = "CONCEPTICON_ID"))

    dbDisconnect(db)

    write_csv(df,'../data/clics/df_all_raw.csv')
} else {
    print('The CSV had already been generated.')
}