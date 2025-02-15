# 安装必要的R包
# if (!requireNamespace("BiocManager", quietly = TRUE))
#   install.packages("BiocManager")
# BiocManager::install("TCGAbiolinks")
# BiocManager::install("survminer")
# BiocManager::install("SummarizedExperiment")
# install.packages("openxlsx")
# 加载必要的R包
library(TCGAbiolinks)
library(survminer)
library(SummarizedExperiment)
library(openxlsx)
# 设置下载目录
download_dir <- "D:/TCGA"
# 获取所有可用的TCGA项目
all_projects <- TCGAbiolinks:::getGDCprojects()
print(all_projects)
# 迭代处理每个TCGA项目
for (i in 1:nrow(all_projects)) {
  # 获取第i行
  row <- all_projects[i, ]
  id <- row$id
  primary_site <- row$primary_site
  dbgap_accession_number <- row$dbgap_accession_number
  project_id <- row$project_id
  disease_type <- row$disease_type
  name <- row$name
  releasable <- row$releasable
  state <- row$state
  released <- row$released
  tumor <- row$tumor

  project.summary <- TCGAbiolinks:::getProjectSummary(project = project_id)
  print(project.summary)
  data_categories <- project.summary$data_categories
  data_category <- data_categories$data_category
  for (category in data_category) {
    all_types <- c(
      "Aggregated Somatic Mutation",
      "Aligned Reads",
      "Gene Expression Quantification",
      "Raw CGI Variant",
      "Methylation Beta Value",
      "Differential Gene Expression",
      "Splice Junction Quantification",
      "Protein Expression Quantification",
      "Annotated Somatic Mutation",
      "Raw Simple Somatic Mutation",
      "Masked Somatic Mutation",
      "Copy Number Segment",
      "Masked Intensities",
      "Allele-specific Copy Number Segment",
      "Masked Copy Number Segment",
      "Isoform Expression Quantification",
      "miRNA Expression Quantification",
      "Gene Level Copy Number",
      "Biospecimen Supplement",
      "Gene Level Copy Number Scores",
      "Protein Expression Quantification",
      "Clinical Supplement",
      "Single Cell Analysis",
      "Masked Somatic Mutation",
      "Slide Image"
    )
    
    for (type in all_types) {
      print(paste("开始处理 TCGA 项目:", project_id))
      print(paste("开始处理 TCGA 类别:", category))
      print(paste("开始处理 TCGA 类型:", type))

      tryCatch({
        query <- GDCquery(
          project = project_id,
          data.category = category,
          data.type = type
        )
        results <- query$results
        print(results)
        for (i in seq_along(results)) {
          result <- results[[i]]
          if (is.data.frame(result)) {
            file_dir <- file.path(download_dir, project_id, category, type)
            print(file_dir)
            dir.create(file_dir, recursive = TRUE, showWarnings = FALSE)
            
            file_name <- paste0("dataframe_", i, ".xlsx")
            file_path <- file.path(file_dir, file_name)
            print(file_path)
            
            openxlsx::write.xlsx(result, file_path, overwrite = TRUE)
            GDCdownload(query, method = "api", directory = download_dir, files.per.chunk = 50)
          } else {
            print("not a dataframe")
          }
        }
      }, error = function(e) {
        print(paste("下载失败信息:", conditionMessage(e)))
      })
    }
  }
}
