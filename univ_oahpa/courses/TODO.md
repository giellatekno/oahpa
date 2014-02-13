# Oppsummering fra prosjektbeskrivelsen:

## Status quo:

* Innloggingssystem basert på Open-ID: brukar får ein konto i kursa, og
  cookie frå kursa/kuvsje gjeld alle subdomainar i `*.oahpa.no`. Oahpa
  ser på cookie:n, og loggar brukaren inn, og registrerar ein ny konto
  viss det trengst.

* Bruk av ulike modular i Oahpa vert logga, og brukaren får oversikt
  over aktivitet, med nokre korte / enkle statistikk

* Admin brukarar for logga inn på ein administrative grensesnitt for å
  leggja til nye lærarar i systemet, og setja deim som ansvarleg i sine
  kurs.

* Admin brukarar får oversikt over elevane deira, og kan sjå på datoen
  av siste innlogging, statistikk, osv. Dette er generert av Django sitt
  admingrensesnittrammeverk.

### Neste stigar

Nye innloggings-/registrasjons- eigenskapar:

 * Studentar får registrera seg i kurs dei fylgjar, og vert knytta opp
   mot ein lærar.

 * Lærar får rettleda studentar om oppgåvor dei bur gjera på ulike trinn
   i kurset.

 * Lærar får oversikt på progresjon i læringsmåla til kvar student,
   resymé

Nye moglegheitar for tilbakemelding til studentar om statistikk / progresjon:

 * Oahpa og View vert logga.

 * Studentane får tilbakemelding på typar grammatiske feil dei gjer

 * Studentar får fylgja med på progresjon i forhold til læringsmål frå
   kurs dei er registrert i: både i form av fargekode for nivå dei hev
   nådd i forhold til læringsmål, og prosent av arbeidsbyrden som er
   definert

Nye moglegheitar for inndeling av oppgåvor:

 * Kurs-spesifiske læringsmål for grammatikk og ordforråd

Nye moglegheitar for grammatiske feedback:

* I forhold til studentane sine nivåklassifisering, får student ulike
  form for tilbakemelding: meir eller mindre faglig grammatisk
  terminologi

* Unngå lange forklaringar: sporing av feedback studentar hev sedd på

## Nye models

 * Student level
   - related course
   - goals completed
   - grammatical feedback type

 * Goal
   - related course
   - goal name
   - expected accuracy rate / condition for success
   - goal definitions:
     - exercise module (MORFA S, MORFA C, LEKSA, NUMRA)
     - exercise settings:
        - semantic sets, or case and number, and so forth
   - goal deep-links

## Endringar på eksisterande model

 * User log - UI events ulik frå correct/incorrect svar: brukar klikkar
   på feedback, opnar grammatikken, osv.

## Nye frontend endringar

 * Systemet må lagra ei loggmelding når studentar klikkar på feedback,
   dvs.: JSON API for logg-eventar

