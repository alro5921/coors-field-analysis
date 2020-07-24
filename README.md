<img src="images/Coors_Pana.jpg" width="700" height="350" />

# Coors Field Analysis

## Motivation

Coors Field is the highest elevation Major League Baseball stadium in the league. Coors Field is at 5200 ft elevation, with the next closest being Arizona's Chase Field at just 1100 ft and the vast majority being within 300 ft of sea level. The thinner and drier air significantly impacts how the ball moves, significantly benefitting the batters; Coors Field is consistently the run leader in the MLB.

Unfortunately, this seems to have a negative impact on Rockies players when they play outside of Coors Field. Iternalizing how pitches move at high altitude may not translate well to other MLB parks, and more aggressive batting styles that produce "borderline" hits at Coors may produce outs elsewhere. 

I'd like to investigate two topics; how strongly playing at Coors produces a negative effect on the road, and what exactly is creating these these disadvantages.


### Scope

I'm restricting data from 2002 onwards, since the Rockies ownership implemented several stadium and ball changes to attempt to decrease the runs scored, most notably the humidor. Yes, it used to be even worse!

<!---
Just have a coors effect section with a few effects? Home runs, hits, 
Graph of ratio vs league av ratio over years?
Show where balls landed?
-->

## Data

I worked primarily with schedule data taken from Retrosheets, [Retrosheets Gamelogs](https://www.retrosheet.org/gamelogs/index.html). Each row contains aggregate stats from a major league baseball game; each team's score, how many hits and what type of hits each team had, who the home and visiting teams were (and w) umpires and their positioning. These contained about 63,000 games since the Rockies' debut in 1993, or about 2,100 at Coors Field* itself.

Which is sort of astounding considering multiple 

I've restricted my analysis to the 2002 season onwards, as the Rockies implemented several stadium and ball changes to decrease the runs scored (most notably a humidor). That cut the games to about 50,000 games and 1,450 games at Coors Field.

The data was complete and comprhes. The fields of interest 

Schedule data, which contain the aggregate stats of each game, was taken from [Retrosheets Gamelogs](https://www.retrosheet.org/gamelogs/index.html). Their data was quite clean, my data cleaning basically consisted of adding headers (with [their reference](https://www.retrosheet.org/gamelogs/glfields.txt)) and dropping (many!) extraenous columns.

>The information used here was obtained free of
>charge from and is copyrighted by Retrosheet.  Interested
>parties may contact Retrosheet at "www.retrosheet.org".

With 2002-2018, we have about 2900 games and 1450 games of Away and Home games at Coors.

*Well, 125 of those games were played at the Bronco's Mile High Stadium as Coors Field was being constructed.

<!---
Statcast pitch-by-pitch data was obtained from Baseball Savant. Statcast has only been tracked to 2008, so any pitch by pitch analysis will be restricted from there.
-->

## Coors Effect
>*There is no folly of the beast of the earth which is not infinitely outdone by the madness of Coors \[Field\].*  
>                                       - Atlanta Braves Commentator



## How Coors affects Players After They Leave


While every baseball team performs worse at visiting stadiums - the league wide "home field advantage" is roughly 54% - the Rockies perform especially badly relative to their home performance. Between 2000-2018, while they've won about 54% of their games at home, they've won just shy of 40% of their games on the road!

One metric is the  I took the ratio of each team's winrate at home and a team's winrate on the road. A team with the league average home advantage would have a .54/.46 ~ 1.17 ratio. The Colorado Rockies are a signficant outlier, with a 1.38 ratio.

![](images/ratio_plot.png)

<!---
Graph of ratio vs league av ratio over years?
-->

# Fatigue
 
One hypothesis is that players are especially fatigued from playing at altitude, from the environment itself and from frequently transiting between altitude. As a litimus test, let's look at their winrate in the first half* of the season vs the second half:

I had initially partitioned this into home/away because 56% of Rockies September games are home games (show this table?) As that'd be an obvious confounder given the huge difference in home/away winrate, I partitioned this into home/away games.

<img src="images/halves.png" width="500" height="500" />

We do see a significant drop in the away winrate between the first half and second half of the season, but oddly enough the home winrate actually rose. A fatigue thing would work regardless of where they're playing. Looking at the month by month data:


<img src="images/monthly_winrates.png" width="600" height="600" />

What we see is not a slow decline from the first half to the second half, but a very strong April road performance (relatively) followed by more uniform performance for the rest of the season.

We can use a chi squared test to check the signifiance of this. We find that the difference between the April Away and the rest of the season is significant,  A quick Chi Squared test suggests the April Away performance is significant, χ^2(1, N = 1498) = 5.93, p = .015, that is it's drawing differently from the rest of the, but the overall Away season χ^2(1, N = 1498) = 5.93, p = .139. 

There doesn't appear to be a pattern in the Home the χ^2(1, N = 1498) = 4.32, p = .505 $$`\chi^2 = \sum \frac {(O - E)^2}{E}`$$

In any case, this data doesn't support a long term fatigue effect throughout the course of the season; we would expect and 

## Home/Away Tradeoff? (Rougher)

From last graph, there seems to be a trade-off between 

Hypothesis: There's a tradeoff between home/away prowess, training towards one detracts from the other. Was a big anti-correlation in home/away winrate in group by months, also the gap is smaller in April (after Spring Training done at a lower altitude field).

Checking the correlation, it's quite low at -.76. And this does seem to be a fairly strong outlier:

![](images/monthly_corrs.png)

Two problems:

1. The Minnesota Twins are also an anticorrelated outlier, and I'm unaware of an equilvent Minnesota park factor that would explain this.
2. The correlations are wide ranged, I would exp
3. I don't know this'd vary so much month by month; if this was a thing I'd expect a gradual shift in either adjusting towards or against Coors Field as the season goes on.

Nonetheless, it's an interesting pattern that seems to at least waggle its eyes at something like a home/away tradeoff.

# Visting Team Fatigue
The Rockies play most of their games at altitude, but what about teams who aren't used to altitude?


## Adjustment

Pitches move differently at Coors Field, particually curveball and "junk" ball pitches. Players have had difficulty adjusting to sea level pitches, as Rockies outfielder Charlie Blackmon explains:

>A pitch follows a peculiar path in the high elevation of Coors Field, but that is Blackmon’s normal. He knows how the arc of a pitch will perform in his home park. He honed that ability over time while watching tens of thousands of pitches there. But the day Blackmon leaves Denver for any of the 25 other cities in the major leagues, the baseball behaves differently...  
>“It’s amazing to see what guys can catch up to. Guys throw 100 now, but people can hit it,” Blackmon said. “It’s amazing what big-league players can do if they see it every day and become accustomed to it. It’s amazing what the level of play has become because the competition is getting so good, right? So for all those reasons, it’s very hard to have a ball act a certain way at altitude, and then have it act noticeably different the very next day when we go on the road."  
>Source: https://theathletic.com/1649617/2020/03/04/inside-the-rockies-new-idea-to-finally-cure-the-coors-field-hangover/ (Paywalled)

<img src="images/road_trip_runs.png" width="720" height="600" />

There's actually a slight downward trend, although it's not signficant. 

This tenatively contradicts the idea of an adjustment period. This could still be a long term thing, where playing at Coors throws off perception for longer than a road trip can "reset".