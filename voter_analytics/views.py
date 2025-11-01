from django.shortcuts import render
from django.views.generic import *
from .models import *
import plotly
import plotly.graph_objs as go
from django.db.models import Count
from django.db.models.functions import ExtractYear

# Create your views here.
class VoterListView(ListView):
    """view showing the list of voters"""
    model = Voter
    template_name = "voter_analytics/show_all_voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """return a queryset to show"""
        qs = super().get_queryset()

        # check if we need to filter by party
        if 'party' in self.request.GET and self.request.GET['party']:
            qs = qs.filter(party_affiliation=self.request.GET['party'])

        # check if we need to filter by min birth year
        if 'min_birth' in self.request.GET and self.request.GET['min_birth']:
            qs = qs.filter(date_of_birth__year__gte=self.request.GET['min_birth'])

        # check if we need to filter by max birth year
        if 'max_birth' in self.request.GET and self.request.GET['max_birth']:
            qs = qs.filter(date_of_birth__year__lte=self.request.GET['max_birth'])

        # check if we need to filter by score
        if 'score' in self.request.GET and self.request.GET['score']:
            qs = qs.filter(voter_score=self.request.GET['score'])

        # check if we need to filter by v20state
        if 'v20state' in self.request.GET and self.request.GET['v20state']:
            qs = qs.filter(v20state=True)

        # check if we need to filter by v21town
        if 'v21town' in self.request.GET and self.request.GET['v21town']:
            qs = qs.filter(v21town=True)

        # check if we need to filter by v21primary
        if 'v21primary' in self.request.GET and self.request.GET['v21primary']:
            qs = qs.filter(v21primary=True)

        # check if we need to filter by v22general
        if 'v22general' in self.request.GET and self.request.GET['v22general']:
            qs = qs.filter(v22general=True)

        # check if we need to filter by v23town
        if 'v23town' in self.request.GET and self.request.GET['v23town']:
            qs = qs.filter(v23town=True)

        return qs
    
    def get_context_data(self, **kwargs):
        """provide context for the view"""
        context = super().get_context_data(**kwargs)

        # add all unique parties to the context for form
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        # add all years for the birth year fields up to voting age
        context['years'] = [1900 + x for x in range(108)]
        # add all scores for the voters
        context['scores'] = [x for x in range(6)]
        # add form data
        context['form'] = self.request.GET

        return context
    

class VoterDetailView(DetailView):
    """view showing the detail of a specific voter"""
    model = Voter
    template_name = "voter_analytics/show_voter.html"
    context_object_name = "voter"


class GraphListView(ListView):
    """view for graphs"""
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self):
        """return a queryset for the forms, borrowed from voterlistview"""
        voter_list_view = VoterListView()
        voter_list_view.request = self.request
        
        return voter_list_view.get_queryset()


    def get_context_data(self, **kwargs):
        """add graph into context for the view"""
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        num_voters = voters.count()

        # data from the orm using annotate() to improve efficiency of query
        data = (voters
                .annotate(year=ExtractYear('date_of_birth'))
                .values('year')
                .annotate(count=Count('id'))
                .order_by('year')
                )
        
        # years for the graph
        years = [d['year'] for d in data]
         # adjust x for right range of years
        if len(years) > 0:
            x = list(range(min(years), max(years) + 1))
        else:
            x = []
        # put data into list y to be displayed in fig
        y = [d['count'] for d in data]
        
        # build the figure and graph and sent to context
        fig = go.Bar(x=x, y=y)
        title = f'Voter distribution by year of birth (n={num_voters})'
        graph_birth_bar = plotly.offline.plot({"data": [fig],
                                               "layout_title_text": title},
                                               auto_open=False,
                                               output_type="div")

        context['graph_birth_bar'] = graph_birth_bar

        # distinct parties
        x = list(voters.values_list('party_affiliation', flat=True).distinct())
        # for each party, find the number of people in that party
        y = [voters.filter(party_affiliation=p).count() for p in x]

        # build fig and graph and send to context
        fig = go.Pie(labels=x, values=y)
        title = f'Voter distribution by party affiliation (n={num_voters})'
        graph_party_pie = plotly.offline.plot({"data": [fig],
                                               "layout_title_text": title},
                                               auto_open=False,
                                               output_type="div")
        
        context['graph_party_pie'] = graph_party_pie

        # all of the events
        x = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        # count people who voted in the event
        y = [voters.filter(**{event: True}).count() for event in x]

        # create the figure, graph, add to context
        fig = go.Bar(x=x, y=y)
        title = f'Voter count by election (n={num_voters})'
        graph_election_bar = plotly.offline.plot({"data": [fig],
                                               "layout_title_text": title},
                                               auto_open=False,
                                               output_type="div")
        
        context['graph_election_bar'] = graph_election_bar

        # add all unique parties to the context for form
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        # add all years for the birth year fields up to voting age
        context['years'] = [1900 + x for x in range(108)]
        # add all scores for the voters
        context['scores'] = [x for x in range(6)]
        # add form data
        context['form'] = self.request.GET

        return context