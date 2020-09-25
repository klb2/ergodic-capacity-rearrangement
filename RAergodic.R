# TODO: Add hint that this is modified from qrmtools
# ...


library("qrmtools")

supermodRA <- function(qF, N, abstol=0, n.lookback=length(qF), max.ra=Inf,
					   sample=TRUE)
{
    # Checks and Step 1 (get N, abstol)
	stopifnot(is.null(abstol) || abstol>=0, length(N)>=1, N>=2,
			  is.logical(sample), is.list(qF), sapply(qF, is.function),
			  (d <- length(qF))>=2, max.ra>d)
	method <- "worst.VaR"

    # Compute lower bound
    ## Step 2 (build \underline{X})
    p <- (0:(N-1))/N
    X.low <- sapply(qF, function(qF) qF(p))
    ## Steps 3--7 (determine \underline{X}^*)
	res.low <- rearrange(X.low, tol=abstol, tol.type="absolute",
						 n.lookback=n.lookback, max.ra=max.ra, method=method,
						 sample=sample, is.sorted=TRUE)

    # Compute upper bound
    ## Step 2 (build \overline{X})
    p <- (1:N)/N
    X.up <- sapply(qF, function(qF) qF(p))
    ### Adjust those that are Inf
    ### use level+(1-level)*(N-1+N)/(2*N) = level+(1-level)*(1-1/(2*N)) instead of 1 quantile
	X.up[N,] <- sapply(1:d,
					   function(j) if(is.infinite(X.up[N,j])) qF[[j]]((1-1/(2*N))) else X.up[N,j])
    ## Step 3--7 (determine \overline{X}^*)
	res.up <- rearrange(X.up, tol=abstol, tol.type="absolute",
						n.lookback=n.lookback, max.ra=max.ra, method=method,
						sample=sample, is.sorted=TRUE)

    # Return
	list(low=res.low$X.rearranged, up=res.up$X.rearranged)
    #list(bounds = c(low = res.low$bound, up = res.up$bound), # (\underline{s}_N, \overline{s}_N)
    #     rel.ra.gap = abs((res.up$bound-res.low$bound)/res.up$bound), # relative RA gap
    #     ind.abs.tol = c(low = res.low$tol, up = res.up$tol), # individual absolute tolerances
    #     converged = c(low = res.low$converged, up = res.up$converged), # converged?
    #     num.ra = c(low = length(res.low$opt.row.sums), up = length(res.up$opt.row.sums)), # number of considered column rearrangements (low, up)
    #     opt.row.sums = list(low = res.low$opt.row.sum, up = res.up$opt.row.sums), # optimal row sums (low, up)
    #     X = list(low = X.low, up = X.up), # input matrices X (low, up)
    #     X.rearranged = list(low = res.low$X.rearranged, up = res.up$X.rearranged), # rearranged Xs (low, up)
    #     X.rearranged.opt.row = # (averaged) rows of X.rearranged leading to the final optimal row sum
    #         list(low = res.low$X.rearranged.opt.row, up = res.up$X.rearranged.opt.row))
}
