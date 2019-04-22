      seqfile = /Users/mlandis/projects/alphavirus_dating/data/emp/mxra8/Mxra8.bovinae.insert_flank.D5.fas       * sequence data filename
      outfile = output/bovidae_plus.insert_flank.L5.M0.NS0.out.txt   * main result file name
      treefile = /Users/mlandis/projects/alphavirus_dating/data/emp/mxra8/mesquite/Mxra8.bovinae.insert.L5.tre

        noisy = 9      * 0,1,2,3,9: how much rubbish on the screen
      verbose = 1      * 1:detailed output
      runmode = 0      * 0:tree

      seqtype = 1      * 1:codons
    CodonFreq = 1      * 0:equal, 1:F1X4, 2:F3X4, 3:F61
        model = 0      * branch-site model
        NSsites = 0    * purifying/neutral/pos selection
        icode = 0      * universal genetic code
        cleandata = 0  * handle codons w/ gaps
* aaDist = 7 * amino acid classes

    fix_kappa = 0      * 1:kappa fixed, 0:kappa to be estimated
        kappa = 2      * initial or fixed kappa

    fix_omega = 0      * 1:omega fixed, 0:omega to be estimated 
        omega = 1      * 1st fixed omega value [change this]
       
