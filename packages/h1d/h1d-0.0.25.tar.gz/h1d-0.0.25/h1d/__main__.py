import argparse
from .MultiTypeScore import *
from .plotMetrics import *
from .plotTwoSample import *
from .MultiSampleScore import *
from .callDirectionalTAD import *

def CLI():
    parser = argparse.ArgumentParser(description="HiC1Dmetrics is a easy to use tools to \
                                                calculate, visualize, and analyze 1D metrics for Hi-C")
    #parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(help="Choose the mode to use sub-commands")

    #Function 1
    def func_basic(args):
        pass
    parser_basic = subparsers.add_parser("basic",help="Provide basic functions to load, handle and visualize Hi-C data.")
    parser_basic.add_argument('mode', type=str, help='Type of 1D metrics,,should be one of {dTAD,stripe,PC1,TAD,hubs}')
    parser_basic.add_argument('matrix', type=str, help='Path of matrix file from JuicerResult')
    parser_basic.add_argument('resolution', type=int,help="Resolution of input matrix")
    parser_basic.add_argument("chromosome",type=str,help="Chromosome number.")
    parser_basic.add_argument("-o","--outname",help="output name",type=str,default="defaultname")
    parser_basic.add_argument('-c','--controlmatrix', type=str, help='Path of control matrix file from JuicerResult',default=None)
    parser_basic.add_argument('--datatype',type=str,help="matrix or rawhic",default="matrix")
    parser_basic.add_argument('--gt',type=str,help="genome table",default="")
    parser_basic.set_defaults(func=func_basic)

    #Function 2
    #=============================================================================
    def func_one(args):
        if args.allchr:
            if datatype not in ["folder","rawhic"]: print("Error: not supported"); exit(1)

        if args.parameter and args.type not in ["PC1","IF"]:
            args.parameter = int(args.parameter)

        score = multiScore(args.matrix,args.resolution,args.chromosome,
                            ).obtainOneScore(args.type,parameter=args.parameter,datatype=args.datatype,gt=args.gt)
        score.to_csv(args.outname + ".bedGraph", sep="\t", header=False, index=False)

        if args.draw:
            if args.allchr: print("Error: not supported"); exit(1)
            if args.type == "IF":
                args.parameter = args.outname + ".bedGraph"
            print("==========output figure==========")
            PlotBedGraph(args.matrix,args.resolution,args.chromosome,startSite=args.start,
                        endSite=args.end,datatype=args.datatype,
                        gt=args.gt).draw(args.type,UniqueParameter=args.parameter)
            plt.savefig(args.outname+".pdf")


    parser_one = subparsers.add_parser("one",help="1D metrics designed for one Hi-C sample",
                                            description="1D metrics designed for one Hi-C sample")
    parser_one.add_argument('type', type=str, help='Type of 1D metrics,,should be one of {IS,CI,DI,SS,DLR,PC1,IES,IAS,IF}')
    parser_one.add_argument('matrix', type=str, help='Path of matrix file from JuicerResult')
    parser_one.add_argument('resolution', type=int,help="Resolution of input matrix")
    parser_one.add_argument("chromosome",type=str,help="Chromosome number.")
    parser_one.add_argument("-p","--parameter",type=str,help="Parameter for indicated metrics",default=None)
    parser_one.add_argument("-o","--outname",help="output name (default metrics)",type=str,default="metrics")
    parser_one.add_argument("-d","--draw",action='store_true',help="Plot figure for candidate region",default=False)
    parser_one.add_argument('--start',type=int,help="Start sites for plotting",default=0)
    parser_one.add_argument('--end',type=int,help="End sites for plotting",default=0)
    parser_one.add_argument('--datatype',type=str,help="matrix or rawhic",default="matrix")
    parser_one.add_argument('--gt',type=str,help="genome table",default="")
    parser_one.add_argument('--allchr',action='store_true',help="Calculate metrics for multiple chromosomes",default=False)
    parser_one.set_defaults(func=func_one)

    #Function 3
    #=============================================================================
    def func_two(args):
        ms = multiScore(args.matrix,args.resolution,args.chromosome,control_path=args.controlmatrix)
        score,path,control_path = ms.obtainTwoScore(args.type,parameter=args.parameter,datatype=args.datatype,gt=args.gt)
        score.to_csv(args.outname + ".bedGraph", sep="\t", header=False, index=False)

        if args.draw:
            if args.type != "IFC":
                DiffDraw(path,control_path,args.resolution,chr = args.chromosome,startSite=args.start,
                        endSite=args.end,datatype="matrix",gt=args.gt).drawMetric("custom",customfile=args.outname + ".bedGraph",name=args.type)
            elif args.type == "IFC":
                DiffDraw(path,control_path,args.resolution,chr = args.chromosome,startSite=args.start,
                        endSite=args.end,datatype="rawhic",gt=args.gt).drawMetric("custom",customfile=args.outname + ".bedGraph",name=args.type)
            plt.savefig(args.outname+".pdf")

        os.system("rm -rf MatrixTemp*")

    parser_two = subparsers.add_parser("two",help="1D metrics designed for comparison of two Hi-C samples",
                                            description="1D metrics designed for comparison of two Hi-C samples")
    parser_two.add_argument('type', type=str, help='Type of 1D metrics,,should be one of {ISC,CIC,SSC,deltaDLR,CD,IESC,IASC,IFC,DRF}')
    parser_two.add_argument('matrix', type=str, help='Path of matrix file from JuicerResult')
    parser_two.add_argument('controlmatrix', type=str, help='Path of control matrix file from JuicerResult')
    parser_two.add_argument('resolution', type=int,help="Resolution of input matrix")
    parser_two.add_argument("chromosome",type=str,help="Chromosome number.")
    parser_two.add_argument("-p","--parameter",type=str,help="Parameter for indicated metrics",default=None)
    parser_two.add_argument("-o","--outname",help="output name (default metrics)",type=str,default="metricsChange")
    parser_two.add_argument("-d","--draw",action='store_true',help="Plot figure for candidate region",default=False)
    parser_two.add_argument('-s','--start',type=int,help="Start sites for plotting",default=0)
    parser_two.add_argument('-e','--end',type=int,help="End sites for plotting",default=0)
    parser_two.add_argument('--datatype',type=str,help="matrix or rawhic",default="matrix")
    parser_two.add_argument('--gt',type=str,help="genome table",default="")
    parser_two.set_defaults(func=func_two)

    #Function 4
    #=============================================================================
    def func_types(args):
        typelist = args.type.split(",")
        parameterlist = args.parameter.split(",")
        if not args.controlmatrix:
            if not set(typelist).issubset(["IS","CI","DI","SS","DLR","PC1","IES","IAS","IF"]):
                print("Error: not supported"); exit(1)
            if "IF" in typelist and args.datatype == "matrix": print("Error: IF required rawhic datatype"); exit(1)
            ms = multiScore(args.matrix,args.resolution,args.chromosome)
            if not args.draw:
                score = ms.allOneScore(typelist,parameterlist,datatype=args.datatype,gt=args.gt)
            elif args.draw:
                score = ms.plotOneScore(typelist,parameterlist,datatype=args.datatype,gt=args.gt,start=args.start,end=args.end)
                plt.savefig(args.outname+".pdf")
            print(score.iloc[550:650,:])
            score.to_csv(args.outname + ".csv", sep="\t", header=True, index=False)
        elif args.controlmatrix:
            if not set(typelist).issubset(["ISC","CIC","SSC","deltaDLR","CD","IESC","IASC","IFC","DRF"]):
                print("Error: not supported"); exit(1)
            if "IFC" in typelist and args.datatype == "matrix": print("Error: IFC required rawhic datatype"); exit(1)
            ms = multiScore(args.matrix,args.resolution,args.chromosome,control_path=args.controlmatrix)
            if not args.draw:
                score = ms.allTwoScore(typelist,parameterlist,datatype=args.datatype,gt=args.gt)
            elif args.draw:
                score = ms.plotTwoScore(typelist,parameterlist,datatype=args.datatype,gt=args.gt,start=args.start,end=args.end)
                plt.savefig(args.outname+".pdf")
            print(score.iloc[550:650,:])
            score.to_csv(args.outname + ".csv", sep="\t", header=True, index=False)

        os.system("rm -rf MatrixTemp*")

    parser_types = subparsers.add_parser("multitypes",help="Various types of 1D metrics for the same sample",
                                            description="Various types of 1D metrics for the same sample")
    parser_types.add_argument('type', type=str, help='Type of 1D metrics,should be {IS,CI,DI,SS,DLR,PC1,IES,IAS,IF} or {ISC,CIC,SSC,deltaDLR,CD,IESC,IASC,IFC,DRF}')
    parser_types.add_argument('matrix', type=str, help='Path of matrix file from JuicerResult')
    parser_types.add_argument('resolution', type=int,help="Resolution of input matrix")
    parser_types.add_argument("chromosome",type=str,help="Chromosome number.")
    parser_types.add_argument("-p","--parameter",type=str,help="Parameter for indicated metrics",default=None,required=True)
    parser_types.add_argument('-c','--controlmatrix', type=str, help='Path of control matrix file from JuicerResult',default=None)
    parser_types.add_argument("-o","--outname",help="output name (default metrics)",type=str,default="multitypes_metrics")
    parser_types.add_argument('--datatype',type=str,help="matrix or rawhic",default="matrix")
    parser_types.add_argument('--gt',type=str,help="genome table",default="")
    parser_types.add_argument("-d","--draw",action='store_true',help="Plot figure for candidate region",default=False)
    parser_types.add_argument('-s','--start',type=int,help="Start sites for plotting",default=0)
    parser_types.add_argument('-e','--end',type=int,help="End sites for plotting",default=0)
    parser_types.set_defaults(func=func_types)

    #Function 5
    #=============================================================================
    def func_samples(args):
        if args.type == "IF" and args.datatype == "matrix": print("Error: IF required rawhic datatype"); exit(1)
        datafile = pd.read_csv(args.txt,sep="\t",header=None)
        labels = list(datafile.iloc[:,0])
        samplelist = list(datafile.iloc[:,1])
        if not args.corr and not args.heat and not args.line:
            score = getMultiSamplesScore(samplelist,labels,args.resolution,args.chromosome,args.type,args.parameter,
                                        datatype=args.datatype,gt=args.gt)
        elif args.corr:
            ms = repQC(samplelist,labels,args.resolution,args.chromosome,args.type,args.parameter,datatype=args.datatype,gt=args.gt)
            score = ms.score
            ms.corr_plot()
            plt.savefig(args.outname+"_corr.pdf")
        elif args.line or args.heat:
            ms = repQC(samplelist,labels,args.resolution,args.chromosome,args.type,args.parameter,datatype=args.datatype,gt=args.gt)
            score = ms.score
            if args.datatype == "matrix":
                plotpath= samplelist[0]
            elif args.datatype == "rawhic":
                plotpath = hic2matrix(samplelist[0],args.resolution,args.chromosome,args.gt)

            if args.heat: plottype = "heat"
            elif args.line: plottype = "line"

            ms.heatmap_tri(plotpath,args.start,args.end,clmax=100,heatmin=None,plottype=plottype)
            plt.savefig(args.outname+"_"+plottype+".pdf")

        score.to_csv(args.outname + ".csv", sep="\t", header=True, index=False)

        print(score.iloc[550:650,:])
        os.system("rm -rf MatrixTemp*")

    parser_samples = subparsers.add_parser("multisamples",help="The same metrics for muliple samples",
                                            description="The same metrics for muliple samples")
    parser_samples.add_argument('type', type=str, help='Type of 1D metrics,,should be one of {IS,CI,DI,SS,DLR,PC1,IES,IAS,IF} or {ISC,CIC,SSC,deltaDLR,CD,IESC,IASC,IFC,DRF}')
    parser_samples.add_argument('resolution', type=int,help="Resolution of input matrix")
    parser_samples.add_argument("chromosome",type=str,help="Chromosome number.")
    parser_samples.add_argument('--datatype',type=str,help="matrix or rawhic",default="matrix")
    parser_samples.add_argument('--txt',type=str,help="a txt contain paths for all samples",default="matrix")
    parser_samples.add_argument('--samplelist', type=str, help='list of file path, can be rawhic or matrix')
    parser_samples.add_argument('--labels', type=str, help='list of file name')
    parser_samples.add_argument("-p","--parameter",type=str,help="Parameter for indicated metrics",default=None)
    parser_samples.add_argument("-o","--outname",help="output name (default metrics)",type=str,default="multisamples_metrics")
    parser_samples.add_argument('--gt',type=str,help="genome table",default="")
    parser_samples.add_argument("--corr",action='store_true',help="Plot correlation for all samples",default=False)
    parser_samples.add_argument("--heat",action='store_true',help="Plot raw heatmap for all samples",default=False)
    parser_samples.add_argument("--line",action='store_true',help="Plot line chart for all samples",default=False)
    parser_samples.add_argument('-s','--start',type=int,help="Start sites for plotting",default=0)
    parser_samples.add_argument('-e','--end',type=int,help="End sites for plotting",default=0)

    parser_samples.set_defaults(func=func_samples)

    #Function 6
    #=============================================================================
    def func_call(args):
        if args.datatype == "rawhic" and args.mode != "hubs":
            path = hic2matrix(args.matrix,args.resolution,args.chromosome,args.gt)
            if args.controlmatrix: controlpath = hic2matrix(args.controlmatrix,args.resolution,args.chromosome,args.gt)
        else:
            path = args.matrix
            controlpath = args.controlmatrix

        if args.mode == "TAD":
            tad = TADcallIS(path,args.resolution,args.chromosome,squareSize=300000)
            tad.to_csv(args.outname + "_TAD.csv", sep="\t", header=True, index=False)
        elif args.mode == "dTAD":
            if not args.controlmatrix: print("Error: DRF requires control data"); exit(1)
            dt = DirectionalTAD(path,controlpath,args.resolution,args.chromosome)
            leftdTAD,rightdTAD,_ = dt.extractRegion()
            leftdTAD.to_csv(args.outname + "_leftdTAD.csv", sep="\t", header=True, index=False)
            rightdTAD.to_csv(args.outname + "_rightdTAD.csv", sep="\t", header=True, index=False)
        elif args.mode == "stripe":
            st = stripeTAD(path,args.resolution,args.chromosome)
            stripe = st.callStripe(squareSize=300000)
            stripe.to_csv(args.outname + "_stripe.csv", sep="\t", header=True, index=False)
        elif args.mode == "hubs":
            if args.datatype != "rawhic": print("Error: hubs requires rawhic datatype"); exit(1)
            IF = InteractionFrequency(path,args.resolution,args.chromosome,gt=args.gt).getIF()
            thresh = np.percentile(IF.iloc[:,3],90)
            hubregion = IF[IF.iloc[:,3]>thresh]
            hubregion.to_csv(args.outname + "_hubs_IF.csv", sep="\t", header=True, index=False)
            os.system("sed '1d' " + args.outname + "_hubs_IF.csv" + " |bedtools merge -i stdin > "+ args.outname + "_hubs.csv")
        else:
            print("unsupported model");exit(1)

    parser_call = subparsers.add_parser("call",help="Extract secondary information from metrics (dTAD, stripeTAD, et.al)",
                                            description="Extract secondary information from metrics (dTAD, stripeTAD, et.al)")
    parser_call.add_argument('mode', type=str, help='Type of 1D metrics,,should be one of {dTAD,stripe,PC1,TAD,hubs}')
    parser_call.add_argument('matrix', type=str, help='Path of matrix file from JuicerResult')
    parser_call.add_argument('resolution', type=int,help="Resolution of input matrix")
    parser_call.add_argument("chromosome",type=str,help="Chromosome number.")
    parser_call.add_argument("-o","--outname",help="output name",type=str,default="defaultname")
    parser_call.add_argument('-c','--controlmatrix', type=str, help='Path of control matrix file from JuicerResult',default=None)
    parser_call.add_argument('--datatype',type=str,help="matrix or rawhic",default="matrix")
    parser_call.add_argument('--gt',type=str,help="genome table",default="")
    parser_call.set_defaults(func=func_call)


    args = parser.parse_args()
    try: func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)
    os.system("rm -rf MatrixTemp*")

if __name__ == '__main__':
    CLI()
